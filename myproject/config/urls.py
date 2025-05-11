from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('lms.urls')),  # Добавь, если планируешь API для LMS
    path('api/users/', include('users.urls')), # Добавь, если планируешь API для Users
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)