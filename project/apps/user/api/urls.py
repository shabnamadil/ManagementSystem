from django.urls import path, re_path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    RegisterAPIView,
    VerifyOTPView,
    ResendOtpView
)

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register-api'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-api'),
    path('resend-otp/', ResendOtpView.as_view(), name='resend-otp-api'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]