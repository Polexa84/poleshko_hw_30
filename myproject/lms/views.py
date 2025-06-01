from rest_framework import viewsets, generics, permissions
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer
from .permissions import IsModerator, IsOwner  # Убедись, что permissions.py находится в той же директории
from rest_framework.permissions import IsAuthenticated

class LessonListAPIView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, (IsModerator | IsOwner)]

class LessonRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, (IsModerator | IsOwner)]

class LessonCreateAPIView(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class LessonUpdateAPIView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, (IsModerator | IsOwner)]

class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator & IsOwner]

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        """
        Определяет права доступа для разных действий.
        """
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated, ~IsModerator]
        elif self.action in ['update', 'partial_update', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated, (IsModerator | IsOwner)]
        elif self.action == 'destroy':
            permission_classes = [permissions.IsAuthenticated, ~IsModerator & IsOwner]
        else:
            permission_classes = [permissions.IsAuthenticated, (IsModerator | IsOwner)] # list
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)