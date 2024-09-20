from django.urls import path, include

from .home.views import HomePageView
from .about.views import AboutPageView
from .contact.views import ContactPageView

urlpatterns = [
    path("", HomePageView.as_view(), name = 'home'),
    path("about/", AboutPageView.as_view(), name = 'about'),
    path("blog/", include('web.blog.urls')),
    path("contact/", ContactPageView.as_view(), name = 'contact'),
]
