from django.urls import path

from .views import (
    WorkspaceListCreateAPIView,
    WorkspaceRetrieveUpdateDestroyAPIView,
    WorkspaceMemberInviteView,
    WorkspaceCategoryListAPIView,
    WorkspaceMemberRemoveView,
    WorkspaceMemberRoleUpdateAPIView,
    ProjectListCreateAPIView,
    ProjectRetrieveUpdateDestoryAPIView,
    ProjectMemberInviteView,
    ProjectMemberRemoveView,
    ProjectMemberRoleUpdateAPIView,
    TaskListCreateAPIView,
    TaskRetriveUpdateDestroyAPIView,
    TaskCompletedAPIView,
    TaskAddMemberAPIView,
    SubtaskListCreateAPIView,
    SubtaskRetrieveUpdateDestroyAPIView,
    SubtaskCompletedAPIView,
    TaskMemberInviteView

)

urlpatterns = [
    path('workspaces/', WorkspaceListCreateAPIView.as_view(), name='workspace-list-api'),
    path('workspaces/<int:pk>/', WorkspaceRetrieveUpdateDestroyAPIView.as_view(), name='workspace-update-destroy'),
    path('workspaces/member/invite/<int:pk>/', WorkspaceMemberInviteView.as_view(), name='workspace-member-invite'),
    path('workspaces/categories/', WorkspaceCategoryListAPIView.as_view(), name='workspace-categories'),
    path('workspaces/member/remove/<int:pk>/', WorkspaceMemberRemoveView.as_view(), name='workspace-member-remove'),
    path('workspaces/member/role/<int:pk>/', WorkspaceMemberRoleUpdateAPIView.as_view(), name="workspace-member-role-update"),
    path('projects/', ProjectListCreateAPIView.as_view(), name='workspace-projects'),
    path('projects/<int:pk>/', ProjectRetrieveUpdateDestoryAPIView.as_view(), name='workspace-projects-update-destroy'),
    path('projects/member/invite/<int:pk>/', ProjectMemberInviteView.as_view(), name='project-member-invite'),
    path('projects/member/remove/<int:pk>/', ProjectMemberRemoveView.as_view(), name='project-member-remove'),
    path('projects/member/role/<int:pk>/', ProjectMemberRoleUpdateAPIView.as_view(), name='project-member-role-update'),
    path('tasks/', TaskListCreateAPIView.as_view(), name="tasks"),
    path('tasks/<int:pk>/', TaskRetriveUpdateDestroyAPIView.as_view(), name="task-update-destroy"),
    path('tasks/completed/<int:pk>/', TaskCompletedAPIView.as_view(), name="task-completed"),
    path('tasks/member/<int:pk>/', TaskAddMemberAPIView.as_view(), name="task-add-member"),
    path('tasks/member/invite/<int:pk>/', TaskMemberInviteView.as_view(), name='task-member-invite'),
    path('subtasks/', SubtaskListCreateAPIView.as_view(), name='subtasks'),
    path('subtasks/<int:pk>/', SubtaskRetrieveUpdateDestroyAPIView.as_view(), name='subtasks-update-destroy'),
    path('subtasks/completed/<int:pk>/', SubtaskCompletedAPIView.as_view(), name="subtask-completed"),
]