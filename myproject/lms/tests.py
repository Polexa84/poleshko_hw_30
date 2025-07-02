'''
# lms/tests.py
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from .models import Course, Lesson, Subscription

User = get_user_model()

# ... остальной код ...
'''