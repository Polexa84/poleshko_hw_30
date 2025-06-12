from rest_framework import serializers
from .models import Course, Lesson, Subscription  # Импортируем Subscription
from .validators import validate_youtube_link  # Импортируем валидатор

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        extra_kwargs = {
            'video_link': {'validators': [validate_youtube_link]}
        }

class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField() # Добавляем поле
    lessons = LessonSerializer(many=True, read_only=True)  # Добавляем поле для уроков
    is_subscribed = serializers.SerializerMethodField()  # Добавляем поле is_subscribed

    class Meta:
        model = Course
        fields = '__all__'  # Или можно указать конкретные поля: ['id', 'title', 'preview', 'description', 'lessons_count', 'is_subscribed']

    def get_lessons_count(self, obj):
        """
        Метод для получения количества уроков для курса.

        Args:
            obj (Course): Объект курса.

        Returns:
            int: Количество уроков для данного курса.
        """
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        """
        Метод для определения, подписан ли текущий пользователь на курс.
        """
        user = self.context.get('request').user
        if user.is_authenticated:
            return Subscription.objects.filter(user=user, course=obj).exists()
        return False