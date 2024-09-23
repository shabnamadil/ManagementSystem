from django.urls import path, re_path

from .views import (
    RegisterAPIView,
    VerifyOTP
)

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register-api'),
    path('verify-otp/', VerifyOTP.as_view(), name='verify-api'),
]