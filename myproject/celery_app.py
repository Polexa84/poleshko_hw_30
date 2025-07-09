import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.config.settings')  # Обратите внимание на путь!

app = Celery('myproject')

# 1. Настройка из Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# 2. Дополнительные настройки
app.conf.update(
    timezone=settings.TIME_ZONE,
    beat_schedule={
        'deactivate-inactive-users': {
            'task': 'users.tasks.deactivate_inactive_users',
            'schedule': crontab(minute=0, hour=3),
        },
    }
)

# 3. Автодискавери задач
app.autodiscover_tasks(
    lambda: [app for app in settings.INSTALLED_APPS
           if not app.startswith('django.')]
)
