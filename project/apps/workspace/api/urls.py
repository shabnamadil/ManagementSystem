from django.urls import path

from .views import WorkspaceListCreateAPIView

urlpatterns = [
    path('workspaces/', WorkspaceListCreateAPIView.as_view(), name='workspace-list-api')
]