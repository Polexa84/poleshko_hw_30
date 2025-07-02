from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from lms.models import Course, Lesson, Subscription

User = get_user_model()

class LessonTestCase(APITestCase):
    """
    Тесты для CRUD операций с уроками.
    """

    def setUp(self):
        """
        Подготовка данных для тестов.
        """
        # Создаем пользователя
        self.user = User.objects.create_user(email='test@example.com', password='testpassword', username='testuser')

        # Создаем модератора
        self.moderator = User.objects.create_user(email='moderator@example.com', password='testpassword', username='moderator')

        # Создаем курс
        self.course = Course.objects.create(title='Test Course', owner=self.user)

        # Создаем урок
        self.lesson = Lesson.objects.create(title='Test Lesson', course=self.course, owner=self.user)

        # Создаем клиент для выполнения запросов
        self.client = APIClient()

        # Аутентифицируем пользователя
        self.client.force_authenticate(user=self.user)

    def test_lesson_list(self):
        """
        Тест: Получение списка уроков.
        """
        url = reverse('lesson-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lesson_retrieve(self):
        """
        Тест: Получение отдельного урока.
        """
        url = reverse('lesson-detail', args=[self.lesson.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)