from rest_framework import serializers
from .models import Course, Lesson

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'  # Или можно указать конкретные поля: ['id', 'title', 'preview', 'description']

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'  # Или можно указать конкретные поля: ['id', 'course', 'title', 'description', 'preview', 'video_link']