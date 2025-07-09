# myproject/__init__.py
from __future__ import absolute_import

# Ленивая загрузка Celery app
def setup_celery():
    from .celery_app import app
    return app

celery_app = setup_celery()
__all__ = ('celery_app',)