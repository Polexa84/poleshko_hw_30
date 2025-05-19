from rest_framework import serializers
from .models import Course, Lesson

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'  # Или можно указать конкретные поля: ['id', 'course', 'title', 'description', 'preview', 'video_link']

class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField() # Добавляем поле
    lessons = LessonSerializer(many=True, read_only=True)  # Добавляем поле для уроков

    class Meta:
        model = Course
        fields = '__all__'  # Или можно указать конкретные поля: ['id', 'title', 'preview', 'description', 'lessons_count']

    def get_lessons_count(self, obj):
        """
        Метод для получения количества уроков для курса.

        Args:
            obj (Course): Объект курса.

        Returns:
            int: Количество уроков для данного курса.
        """
        return obj.lessons.count()
