from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

@shared_task
def deactivate_inactive_users():
    """Деактивирует пользователей, не заходивших в систему более месяца."""
    User = get_user_model()
    inactive_date = timezone.now() - timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lte=inactive_date, is_active=True)

    for user in inactive_users:
        user.is_active = False
        user.save()
        print(f"Пользователь {user.username} деактивирован.")  # Логирование (опционально)