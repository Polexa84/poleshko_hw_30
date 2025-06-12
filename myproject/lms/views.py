from rest_framework import viewsets, generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Course, Lesson, Subscription
from .serializers import CourseSerializer, LessonSerializer
from .permissions import IsModerator, IsOwner
from rest_framework.permissions import IsAuthenticated
from .paginators import CoursePaginator, LessonPaginator  # Импортируем пагинаторы
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes  # Импортируем декоратор и OpenApiParameter


@extend_schema(
    summary='Получение списка уроков',
    description='Этот эндпоинт возвращает список всех доступных уроков.',
    responses={200: LessonSerializer(many=True)}
)
class LessonListAPIView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, (IsModerator | IsOwner)]  # Просмотр доступен всем аутентифицированным, модераторам и владельцам
    pagination_class = LessonPaginator  # Добавляем пагинатор


@extend_schema(
    summary='Получение информации об уроке',
    description='Этот эндпоинт возвращает детальную информацию об уроке по его ID.',
    responses={200: LessonSerializer}
)
class LessonRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, (IsModerator | IsOwner)]  # Просмотр доступен всем аутентифицированным, модераторам и владельцам


@extend_schema(
    summary='Создание урока',
    description='Этот эндпоинт позволяет создать новый урок.',
    responses={201: LessonSerializer},
    request=LessonSerializer
)
class LessonCreateAPIView(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]  # Создание доступно только аутентифицированным пользователям, не модераторам

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)  # Автоматическая установка владельца


@extend_schema(
    summary='Обновление урока',
    description='Этот эндпоинт позволяет обновить существующий урок.',
    responses={200: LessonSerializer},
    request=LessonSerializer
)
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
