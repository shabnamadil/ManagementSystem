from django.urls import path

from .views.login_page import LoginPageView
from .views.logout import logout_view

urlpatterns = [
    path("login/", LoginPageView.as_view(), name = 'login'),
    path('logout/', logout_view, name = "logout"),
]
