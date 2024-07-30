from django.urls import path
from .views.workspaces_page import WorkspacePageView

urlpatterns = [
    path("", WorkspacePageView.as_view(), name = 'workspaces')
    # path('workspaces/', views.WorkspacesPageView.as_view(), name = 'workspaces'),
    # path('workspaces/<slug:slug>/', views.WorkspaceDetailPageView.as_view(), name = 'workspace-detail'),
    # path('create-workspace/', views.WorkspaceCreateAPIView.as_view(), name = 'create-workspace'),

    # path('workspaces/<slug:slug>/<slug:project_slug>/tasks/', views.TasksPageView.as_view(), name = 'tasks'),
]
