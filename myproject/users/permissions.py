from rest_framework import permissions

class IsModerator(permissions.BasePermission):
    """
    Проверяет, является ли пользователь модератором.
    """
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Модераторы').exists()

class IsNotCreator(permissions.BasePermission):
    """
    Запрещает создание объектов.
    """
    def has_permission(self, request, view):
        if request.method == 'POST':
            return False
        return True

class IsNotDeletor(permissions.BasePermission):
    """
    Запрещает удаление объектов.
    """
    def has_permission(self, request, view):
        if request.method == 'DELETE':
            return False
        return True