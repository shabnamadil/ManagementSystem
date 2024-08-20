from django.urls import path, re_path

from .views.workspaces_page import WorkspacePageView
from .views.accept_invitation import accept_invitation
from .views.workspace_detail import WorkspaceDetailView


urlpatterns = [
    path("", WorkspacePageView.as_view(), name = 'workspaces'),
    re_path(
        r'^workspace-accept-invite/(?P<uid>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z_\-]+)/(?P<email>[^/]+)/$',
        accept_invitation,
        name='workspace-accept-invite'
    ),
    path('workspaces/<slug:slug>/', WorkspaceDetailView.as_view(), name = 'workspace-detail'),
    # path('create-workspace/', views.WorkspaceCreateAPIView.as_view(), name = 'create-workspace'),

    # path('workspaces/<slug:slug>/<slug:project_slug>/tasks/', views.TasksPageView.as_view(), name = 'tasks'),
]
