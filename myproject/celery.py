import os
from celery import Celery
from django.conf import settings
#from celery.schedules import crontab  # Уберем, так как используем django-celery-beat

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.config.settings')

app = Celery('myproject')

# Load celery config from settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# Optional: Timezone setting.  Can also be done in settings.py
# app.conf.timezone = settings.TIME_ZONE

# Autodiscover tasks - use this if your tasks are in Django apps
from django.apps import apps
app.autodiscover_tasks(lambda: [app_config.name for app_config in apps.get_app_configs()])

# Optional: Add schedule with django-celery-beat.  Remove this section if not using beat
# from celery.schedules import crontab
# app.conf.beat_schedule = {
#     'deactivate-inactive-users': {
#         'task': 'users.tasks.deactivate_inactive_users',
#         'schedule': crontab(minute=0, hour=3),
#     },
# }