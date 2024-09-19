from django.urls import path, include

from .home.views import HomePageView

urlpatterns = [
    path("", HomePageView.as_view(), name = 'home'),
]
