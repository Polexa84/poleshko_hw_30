from rest_framework import generics, permissions
from .models import Payment
from .serializers import PaymentSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import PaymentFilter
from django.conf import settings
from django.apps import apps  # Импортируем apps
User = apps.get_model(settings.AUTH_USER_MODEL)  # Получаем модель пользователя
from .serializers import UserSerializer, RegisterSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class PaymentListAPIView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PaymentFilter


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)