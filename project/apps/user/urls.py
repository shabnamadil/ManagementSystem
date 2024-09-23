from django.urls import path, re_path

from .views.login_page import LoginPageView
from .views.logout import logout_view
from .views.register_page import RegisterPageView
from .views.verify_register import VerifyRegisterPageView

urlpatterns = [
    path("login/", LoginPageView.as_view(), name = 'login'),
    path("register/", RegisterPageView.as_view(), name = 'register'),
    path("verify/", VerifyRegisterPageView.as_view(), name = 'verify'),
    path('logout/', logout_view, name = "logout"),
]
