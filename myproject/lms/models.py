from django.db import models
from django.conf import settings  # Импортируем settings


class Course(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    preview = models.ImageField(upload_to='courses/', blank=True, null=True, verbose_name='Превью')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Владелец',
                              related_name='courses')  # Добавлено поле owner
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Цена')  # Цена курса
    last_update = models.DateTimeField(blank=True, null=True, verbose_name='Последнее обновление')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        app_label = 'lms'


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons', verbose_name='Курс')
    title = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    preview = models.ImageField(upload_to='lessons/', blank=True, null=True, verbose_name='Превью')
    video_link = models.URLField(blank=True, null=True, verbose_name='Ссылка на видео')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Владелец',
                              related_name='lessons')  # Добавлено поле owner

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscriptions',
                             verbose_name='Пользователь')
    course = models.ForeignKey('lms.Course', on_delete=models.CASCADE, related_name='subscriptions',
                               verbose_name='Курс')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        unique_together = ('user', 'course')  # Один пользователь может быть подписан на курс только один раз

    def __str__(self):
        return f'{self.user.email} - {self.course.title}'


class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата оплаты')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма оплаты')
    payment_method = models.CharField(max_length=100, verbose_name='Способ оплаты', default='card')
    stripe_product_id = models.CharField(max_length=255, blank=True, null=True, verbose_name='ID продукта Stripe')
    stripe_price_id = models.CharField(max_length=255, blank=True, null=True, verbose_name='ID цены Stripe')
    stripe_session_id = models.CharField(max_length=255, blank=True, null=True, verbose_name='ID сессии Stripe')
    status = models.CharField(max_length=50, verbose_name='Статус оплаты', default='pending')

    def __str__(self):
        return f"Оплата {self.amount} за курс {self.course} пользователем {self.user}"

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'