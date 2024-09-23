from django.urls import path, include

from .views import FreelancerPageView

urlpatterns = [
    path("", FreelancerPageView.as_view(), name = 'freelancer'),
]
