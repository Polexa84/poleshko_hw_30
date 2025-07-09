import os
from celery import Celery

# Установка переменной окружения Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

app = Celery('myproject')

# Конфигурация из settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# Отложенная настройка (после полной загрузки Django)
@app.on_after_configure.connect
def setup_celery(sender, **kwargs):
    from django.conf import settings
    sender.conf.timezone = settings.TIME_ZONE
    sender.conf.beat_schedule = {
        'deactivate-inactive-users': {
            'task': 'users.tasks.deactivate_inactive_users',
            'schedule': 86400,  # 24 часа в секундах
        }
    }

app.autodiscover_tasks()