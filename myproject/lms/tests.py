from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from lms.models import Course, Lesson, Subscription

User = get_user_model()

