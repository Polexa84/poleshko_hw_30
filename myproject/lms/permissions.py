from rest_framework import permissions

class IsModerator(permissions.BasePermission):
    """
    Разрешает доступ только пользователям из группы "Модераторы".
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name='Модераторы').exists()

class IsOwner(permissions.BasePermission):
    """
    Разрешает доступ только владельцам объектов.
    """
    def has_object_permission(self, request, view, obj):
        # Разрешаем только владельцам объекты
        return obj.owner == request.user