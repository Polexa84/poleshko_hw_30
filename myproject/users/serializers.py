from rest_framework import serializers
from .models import Payment
from django.conf import settings
from django.apps import apps
User = apps.get_model(settings.AUTH_USER_MODEL)
from django.contrib.auth.hashers import make_password


class PaymentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Payment.
    """
    class Meta:
        model = Payment
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели User.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'is_staff']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        Создает нового пользователя. Пароль хешируется перед сохранением.
        """
        validated_data['password'] = make_password(validated_data['password'])
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Обновляет существующего пользователя. Если передан пароль, он хешируется.
        """
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().update(instance, validated_data)


class RegisterSerializer(serializers.ModelSerializer):
    """
    Сериализатор для регистрации новых пользователей.
    """
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """
        Создает нового пользователя при регистрации. Пароль хешируется.
        """
        validated_data['password'] = make_password(validated_data['password'])
        return User.objects.create(**validated_data)