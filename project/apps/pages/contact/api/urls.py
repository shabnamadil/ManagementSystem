from django.urls import path
from .views import ContactPostAPIView

urlpatterns = [
    path('contact/', ContactPostAPIView.as_view(), name='contact-post')
]