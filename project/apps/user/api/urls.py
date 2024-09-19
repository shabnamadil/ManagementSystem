from django.urls import path, re_path

from .views import (
    RegisterAPIView
)

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
]