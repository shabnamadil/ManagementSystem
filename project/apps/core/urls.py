from django.urls import path, include
from .views.dashboard_page import DashboardPageView

urlpatterns = [
    path("", DashboardPageView.as_view(), name = 'dashboard'),
    path("workspaces/", include("apps.workspace.urls")),
    path("", include("apps.user.urls"))
    # path('workspaces/', views.WorkspacesPageView.as_view(), name = 'workspaces'),
    # path('workspaces/<slug:slug>/', views.WorkspaceDetailPageView.as_view(), name = 'workspace-detail'),
    # path('create-workspace/', views.WorkspaceCreateAPIView.as_view(), name = 'create-workspace'),

    # path('workspaces/<slug:slug>/<slug:project_slug>/tasks/', views.TasksPageView.as_view(), name = 'tasks'),
]
