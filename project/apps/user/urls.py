from django.urls import path, re_path

from .views.login_page import LoginPageView
from .views.logout import logout_view
from .views.account_activation import activate

urlpatterns = [
    path("login/", LoginPageView.as_view(), name = 'login'),
    path('logout/', logout_view, name = "logout"),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,2033})/$', 
        activate, name='activate'),
]
