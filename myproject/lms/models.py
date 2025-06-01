from django.db import models

class Course(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    preview = models.ImageField(upload_to='courses/', blank=True, null=True, verbose_name='Превью')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons', verbose_name='Курс')
    title = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    preview = models.ImageField(upload_to='lessons/', blank=True, null=True, verbose_name='Превью')
    video_link = models.URLField(blank=True, null=True, verbose_name='Ссылка на видео')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'