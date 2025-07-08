import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

# Установите переменную окружения DJANGO_SETTINGS_MODULE
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.config.settings')

app = Celery('myproject')

# Настройка Celery из settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# Настройка расписания Celery Beat
app.conf.beat_schedule = {
    'deactivate-inactive-users': {
        'task': 'users.tasks.deactivate_inactive_users',  # Полный путь к задаче Celery
        'schedule': crontab(minute=0, hour=3),  # Запускать задачу каждый день в 3:00
    },
}

app.conf.timezone = settings.TIME_ZONE

# Автоматическое обнаружение задач в приложениях Django
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')