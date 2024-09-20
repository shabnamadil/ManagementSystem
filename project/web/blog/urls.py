from django.urls import path, include

from .views import BlogPageView

urlpatterns = [
    path("", BlogPageView.as_view(), name = 'blog'),
]
