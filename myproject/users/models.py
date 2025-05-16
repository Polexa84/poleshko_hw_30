from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager  # Импортируем наш UserManager

class User(AbstractUser):
    username = None  # Убираем username
    email = models.EmailField(unique=True, verbose_name='Email')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Телефон')
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name='Город')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Аватарка')

    USERNAME_FIELD = 'email'  # Указываем email как поле для аутентификации
    REQUIRED_FIELDS = []  # Список полей, которые нужно заполнить при создании суперпользователя

    objects = UserManager()  # Используем наш UserManager

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'