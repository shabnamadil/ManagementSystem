from django.urls import path
from .views import NewsletterPostAPIView

urlpatterns = [
    path('newsletter/', NewsletterPostAPIView.as_view(), name='newsletter')
]