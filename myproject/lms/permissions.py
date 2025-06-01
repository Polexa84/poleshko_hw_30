from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Проверяет, является ли пользователь владельцем объекта.
    """
    def has_object_permission(self, request, view, obj):
        # Разрешаем только владельцам объекты
        return obj.owner == request.user