from django.urls import path, re_path

from .views.workspaces_page import WorkspacePageView
from .views.workspace_detail import WorkspaceDetailView
from .views.project_detail import ProjectDetailView
from .views.task_detail import TaskDetailView
from .views.workspace_accept_invitation import workspace_accept_invitation
from .views.project_accept_invitation import project_accept_invitation
from .views.task_accept_invitation import task_accept_invitation

urlpatterns = [
    path("", WorkspacePageView.as_view(), name='workspaces'),
    path('<int:pk>/', WorkspaceDetailView.as_view(), name='workspace-detail'),
    path('project/<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    re_path(
        r'^workspace-accept-invite/(?P<uid>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z_\-]+)/(?P<email>[^/]+)/$',
        workspace_accept_invitation,
        name='workspace-accept-invite'
    ),
    re_path(
        r'^project-accept-invite/(?P<uid>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z_\-]+)/(?P<email>[^/]+)/$',
        project_accept_invitation,
        name='project-accept-invite'
    ),
    re_path(
        r'^task-accept-invite/(?P<uid>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z_\-]+)/(?P<email>[^/]+)/$',
        task_accept_invitation,
        name='task-accept-invite'
    ),
    # path('create-workspace/', views.WorkspaceCreateAPIView.as_view(), name = 'create-workspace'),

    # path('workspaces/<slug:slug>/<slug:project_slug>/tasks/', views.TasksPageView.as_view(), name = 'tasks'),
]
