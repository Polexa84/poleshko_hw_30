from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager  # Импортируем наш UserManager

class User(AbstractUser):
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
        app_label = 'users'


class Payment(models.Model):
    """
    Модель для хранения информации о платежах пользователей за курсы и уроки.
    """
    PAYMENT_METHODS = (
        ('cash', 'Наличные'),
        ('transfer', 'Перевод на счет'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь',
                             related_name='users_payments')  # Добавлен related_name
    payment_date = models.DateField(verbose_name='Дата оплаты')
    paid_course = models.ForeignKey('lms.Course', on_delete=models.SET_NULL, blank=True, null=True,
                                    verbose_name='Оплаченный курс',
                                    related_name='users_payments')  # Добавлен related_name
    paid_lesson = models.ForeignKey('lms.Lesson', on_delete=models.SET_NULL, blank=True, null=True,
                                    verbose_name='Оплаченный урок',
                                    related_name='users_payments')  # Добавлен related_name
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма оплаты')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, verbose_name='Способ оплаты')

    def __str__(self):
        return f"Платеж {self.user} - {self.payment_amount} ({self.payment_date})"

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
        app_label = 'users'