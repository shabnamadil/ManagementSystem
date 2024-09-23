from django.urls import path, include

from .views.dashboard import DashboardPageView

urlpatterns = [
    path("", DashboardPageView.as_view(), name = 'dashboard'),
]
