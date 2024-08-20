from django.urls import path

from .views import (
    WorkspaceListCreateAPIView,
    WorkspaceRetrieveUpdateDestroyAPIView,
    WorkspaceMemberInviteView,
    WorkspaceCategoryListAPIView,
    WorkspaceMemberRemoveView,
    WorkspaceMemberRoleUpdateAPIView,
    ProjectListCreateAPIView,
    ProjectRetrieveUpdateDestoryAPIView

)

urlpatterns = [
    path('workspaces/', WorkspaceListCreateAPIView.as_view(), name='workspace-list-api'),
    path('workspaces/<int:pk>/', WorkspaceRetrieveUpdateDestroyAPIView.as_view(), name='workspace-update-destroy'),
    path('workspaces/member/invite/<int:pk>/', WorkspaceMemberInviteView.as_view(), name='workspace-member-invite'),
    path('workspaces/categories/', WorkspaceCategoryListAPIView.as_view(), name='workspace-categories'),
    path('workspaces/member/remove/<int:pk>/', WorkspaceMemberRemoveView.as_view(), name='workspace-member-remove'),
    path('workspaces/member/role/<int:pk>/', WorkspaceMemberRoleUpdateAPIView.as_view(), name="workspace-member-role-update"),
    path('workspaces/projects/', ProjectListCreateAPIView.as_view(), name='workspace-projects'),
    path('workspaces/projects/<int:pk>/', ProjectRetrieveUpdateDestoryAPIView.as_view(), name='workspace-projects-update-destroy'),
]