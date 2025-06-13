from rest_framework import viewsets, generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Course, Lesson, Subscription, Payment
from .serializers import CourseSerializer, LessonSerializer, PaymentSerializer
from .permissions import IsModerator, IsOwner
from rest_framework.permissions import IsAuthenticated
from .paginators import CoursePaginator, LessonPaginator
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from .stripe_service import create_stripe_product, create_stripe_price, create_stripe_checkout_session, retrieve_stripe_checkout_session
from django.utils import timezone
from datetime import timedelta
from .tasks import send_course_update_email  # Импортируем задачу Celery


class LessonListAPIView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, (IsModerator | IsOwner)]  # Просмотр доступен всем аутентифицированным, модераторам и владельцам
    pagination_class = LessonPaginator  # Добавляем пагинатор


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, (IsModerator | IsOwner)]  # Просмотр доступен всем аутентифицированным, модераторам и владельцам


class LessonCreateAPIView(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]  # Создание доступно только аутентифицированным пользователям, не модераторам

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)  # Автоматическая установка владельца


class LessonUpdateAPIView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, (IsModerator | IsOwner)]  # Редактирование доступно всем аутентифицированным, модераторам и владельцам


@extend_schema(
    summary='Удаление урока',
    description='Этот эндпоинт позволяет удалить урок.',
    responses={204: None}  # Указываем None, так как в ответе нет тела
)
class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator & IsOwner]  # Удаление доступно только владельцам, не модераторам


@extend_schema(
    summary='Курсы',
    description='Этот ViewSet предоставляет CRUD операции для курсов.',
    responses={200: CourseSerializer(many=True)}  # Пример ответа для list
)
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CoursePaginator  # Добавляем пагинатор
    permission_classes = [IsAuthenticated, (IsModerator | IsOwner)]

    def get_permissions(self):
        """
        Определяет права доступа для разных действий.
        """
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated, ~IsModerator]  # Создание курса
        elif self.action in ['update', 'partial_update', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated, (IsModerator | IsOwner)]  # Просмотр/Редактирование курса
        elif self.action == 'destroy':
            permission_classes = [permissions.IsAuthenticated, ~IsModerator & IsOwner]  # Удаление курса
        else:
            permission_classes = [permissions.IsAuthenticated, (IsModerator | IsOwner)]  # list
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)  # Автоматическая установка владельца

    def get_serializer_context(self):
        """
        Добавляем request в контекст сериализатора.
        """
        return {'request': self.request}


@extend_schema(
    summary='Подписка на курс',
    description='Этот эндпоинт позволяет подписаться или отписаться от курса.',
    request=None,  # Указываем None, так как тело запроса обрабатывается вручную
    responses={
        200: {
            'type': 'object',
            'properties': {
                'message': {
                    'type': 'string',
                    'description': 'Сообщение об успехе'
                }
            }
        },
        400: {
            'type': 'object',
            'properties': {
                'error': {
                    'type': 'string',
                    'description': 'Сообщение об ошибке'
                }
            }
        }
    },
    parameters=[
        OpenApiParameter(
            name='course_id',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,  # Указываем, что это query-параметр
            description='ID курса для подписки/отписки',
            required=True,  # Указываем, что параметр обязателен
        ),
    ]
)
class SubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')

        if not course_id:
            return Response({"error": "Необходимо указать course_id"}, status=status.HTTP_400_BAD_REQUEST)

        course_item = get_object_or_404(Course, pk=course_id)
        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = 'подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = 'подписка добавлена'

        return Response({"message": message}, status=status.HTTP_200_OK)


class CreatePaymentView(APIView):
    def post(self, request, course_id):
        try:
            course = Course.objects.get(pk=course_id)
            amount = int(course.price * 100)  # Цена в центах
            success_url = request.build_absolute_uri(f'/payment/success/{course_id}/')  # URL для успешной оплаты
            cancel_url = request.build_absolute_uri(f'/payment/cancel/{course_id}/')  # URL для отмены оплаты

            # 1. Создаем продукт в Stripe
            stripe_product = create_stripe_product(name=course.title, description=course.description)

            # 2. Создаем цену в Stripe
            stripe_price = create_stripe_price(product_id=stripe_product.id, unit_amount=amount)

            # 3. Создаем сессию оформления заказа в Stripe
            stripe_session = create_stripe_checkout_session(
                price_id=stripe_price.id,
                success_url=success_url,
                cancel_url=cancel_url
            )

            # 4. Сохраняем информацию об оплате в нашей базе данных
            payment = Payment.objects.create(
                user=request.user,
                course=course,
                amount=course.price,
                stripe_product_id=stripe_product.id,
                stripe_price_id=stripe_price.id,
                stripe_session_id=stripe_session.id,
                status='pending'
            )

            serializer = PaymentSerializer(payment)  # Сериализуем данные об оплате
            return Response({'session_url': stripe_session.url, 'payment': serializer.data}, status=status.HTTP_200_OK)

        except Course.DoesNotExist:
            return Response({'error': 'Курс не найден'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PaymentSuccessView(APIView):
    def get(self, request, course_id):
        try:
            payment = Payment.objects.get(user=request.user, course_id=course_id, status='pending')
            session = retrieve_stripe_checkout_session(payment.stripe_session_id)

            if session.payment_status == 'paid':
                payment.status = 'paid'
                payment.save()
                return Response({'message': 'Оплата успешно завершена'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Оплата не завершена'}, status=status.HTTP_400_BAD_REQUEST)

        except Payment.DoesNotExist:
            return Response({'error': 'Платеж не найден'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PaymentCancelView(APIView):
    def get(self, request, course_id):
        return Response({'message': 'Оплата отменена'}, status=status.HTTP_200_OK)


class CourseUpdateAPIView(generics.UpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, (IsModerator | IsOwner)]  # или какие у тебя там права доступа

    def perform_update(self, serializer):
        course = self.get_object()
        last_update = course.last_update  # Получаем last_update

        if last_update is None or (timezone.now() - last_update) > timedelta(hours=4):
            serializer.save()
            course.last_update = timezone.now()
            course.save()

            # Отправка уведомлений подписчикам
            subscriptions = Subscription.objects.filter(course=course)
            recipient_list = [subscription.user.email for subscription in subscriptions]

            if recipient_list:
                subject = f"Обновление курса: {course.title}"
                message = f"Курс '{course.title}' был обновлен. Пожалуйста, проверьте новые материалы."
                # Вызываем задачу Celery асинхронно
                send_course_update_email.delay(course.id, subject, message, recipient_list)
        else:
            serializer.save()