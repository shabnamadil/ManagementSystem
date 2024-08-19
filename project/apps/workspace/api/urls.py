from django.urls import path

from .views import (
    WorkspaceListCreateAPIView,
    WorkspaceRetrieveUpdateDestroyAPIView,
    WorkspaceMemberInviteView,
    WorkspaceCategoryListAPIView,
    WorkspaceMemberRemoveView,
    WorkspaceMemberRoleUpdateAPIView
)

urlpatterns = [
    path('workspaces/', WorkspaceListCreateAPIView.as_view(), name='workspace-list-api'),
    path('workspaces/<int:pk>/', WorkspaceRetrieveUpdateDestroyAPIView.as_view(), name='workspace_update_destroy'),
    path('workspaces/member/invite/<int:pk>/', WorkspaceMemberInviteView.as_view(), name='workspace_member_invite'),
    path('workspaces/categories/', WorkspaceCategoryListAPIView.as_view(), name='workspace_categories'),
    path('workspaces/member/remove/<int:pk>/', WorkspaceMemberRemoveView.as_view(), name='workspace-member-remove'),
    path('workspaces/member/role/<int:pk>/', WorkspaceMemberRoleUpdateAPIView.as_view(), name="workspace-member-role-update")
]