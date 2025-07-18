from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, LessonListAPIView, LessonRetrieveAPIView, LessonCreateAPIView, LessonUpdateAPIView, LessonDestroyAPIView, SubscriptionAPIView  # Импортируем SubscriptionAPIView

router = DefaultRouter()
router.register(r'courses', CourseViewSet)  # Маршруты для CourseViewSet

urlpatterns = [
    path('', include(router.urls)), # Подключаем маршруты из router

    path('lessons/', LessonListAPIView.as_view(), name='lesson-list'),
    path('lessons/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson-detail'),
    path('lessons/create/', LessonCreateAPIView.as_view(), name='lesson-create'),
    path('lessons/<int:pk>/update/', LessonUpdateAPIView.as_view(), name='lesson-update'),
    path('lessons/<int:pk>/delete/', LessonDestroyAPIView.as_view(), name='lesson-delete'),
    path('subscriptions/', SubscriptionAPIView.as_view(), name='subscription-manage'),  # Добавляем URL для SubscriptionAPIView
]