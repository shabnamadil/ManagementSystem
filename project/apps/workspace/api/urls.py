from django.urls import path

from .views import (
    WorkspaceListCreateAPIView,
    WorkspaceRetrieveUpdateDestroyAPIView,
    WorkspaceMemberInviteView,
    WorkspaceCategoryListAPIView
)

urlpatterns = [
    path('workspaces/', WorkspaceListCreateAPIView.as_view(), name='workspace-list-api'),
    path('workspaces/<int:pk>/', WorkspaceRetrieveUpdateDestroyAPIView.as_view(), name='workspace_update_destroy'),
    path('workspaces/member/invite/<slug:slug>/', WorkspaceMemberInviteView.as_view(), name='workspace_member_invite'),
    path('workspaces/categories/', WorkspaceCategoryListAPIView.as_view(), name='workspace_categories')
]