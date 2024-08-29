from rest_framework.generics import (
    CreateAPIView,
    ListCreateAPIView, 
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
    UpdateAPIView,
    RetrieveUpdateAPIView
)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import (
    WorkspaceListSerializer,
    WorkspacePostSerializer,
    WorkspaceMemberInvitationSerializer,
    WorkspaceCategoryListSerializer,
    WorkspaceMemberRemoveSerializer,
    WorkspaceMemberRoleUpdateSerializer,
    ProjectListSerializer,
    ProjectPostSerializer,
    ProjectMemberInvitationSerializer,
    ProjectMemberRemoveSerializer,
    ProjectMemberRoleUpdateSerializer,
    TaskListSerializer,
    TaskPostSerializer,
    TaskCompletedSerializer,
    TaskAddMemberSerializer,
    TaskMemberInvitationSerializer,
    SubtaskListSerializer,
    SubtaskPostSerializer,
    SubtaskCompletedSerializer
)

from .repositories import (
    WorkspaceRepository,
    WorkspaceProjectRepository,
    TaskRepository,
    SubtaskRepository
)
from apps.workspace.models import (
    Workspace,
    WorkspaceCategory,
    WorkspaceProject,
    Task,
    Subtask
)

class WorkspaceListCreateAPIView(ListCreateAPIView):
    serializer_class = WorkspaceListSerializer
    queryset = Workspace.objects.filter(is_banned=False)
    repo = WorkspaceRepository

    def get_serializer_class(self):
        if self.request.method == 'POST' :
            self.serializer_class = WorkspacePostSerializer
        return super().get_serializer_class()

    def get_filter_methods(self):
        repo = self.repo()
        return {
            'creator' : repo.get_by_creator,
        }

    def get_queryset(self, **kwargs):
        filters = self.get_filter_methods()
        qs = Workspace.objects.filter(is_banned=False)
        for key, value in self.request.query_params.items():
            if key in filters:
                qs = filters[key](value, qs)
        return qs
    

class WorkspaceRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = WorkspacePostSerializer
    queryset = Workspace.objects.filter(is_banned=False)


class WorkspaceMemberInviteView(UpdateAPIView):
    serializer_class = WorkspaceMemberInvitationSerializer
    queryset = Workspace.objects.filter(is_banned=False)


class WorkspaceCategoryListAPIView(ListAPIView):
    serializer_class = WorkspaceCategoryListSerializer
    queryset = WorkspaceCategory.objects.all()


class WorkspaceMemberRemoveView(UpdateAPIView):
    serializer_class = WorkspaceMemberRemoveSerializer
    queryset = Workspace.objects.filter(is_banned=False)


class WorkspaceMemberRoleUpdateAPIView(UpdateAPIView):
    serializer_class = WorkspaceMemberRoleUpdateSerializer
    queryset = Workspace.objects.filter(is_banned=False)


class ProjectListCreateAPIView(ListCreateAPIView):
    serializer_class = ProjectListSerializer
    queryset = WorkspaceProject.objects.all()
    repo = WorkspaceProjectRepository

    def get_serializer_class(self):
        if self.request.method == 'POST' :
            self.serializer_class = ProjectPostSerializer
        return super().get_serializer_class()
    
    def get_filter_methods(self):
        repo = self.repo()
        return {
            'workspace' : repo.get_by_workspace,
        }

    def get_queryset(self, **kwargs):
        filters = self.get_filter_methods()
        qs = WorkspaceProject.objects.all()
        for key, value in self.request.query_params.items():
            if key in filters:
                qs = filters[key](value, qs)
        return qs


class ProjectRetrieveUpdateDestoryAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectPostSerializer
    queryset = WorkspaceProject.objects.all()


class ProjectMemberInviteView(UpdateAPIView):
    serializer_class = ProjectMemberInvitationSerializer
    queryset = WorkspaceProject.objects.all()


class ProjectMemberRemoveView(UpdateAPIView):
    serializer_class = ProjectMemberRemoveSerializer
    queryset = WorkspaceProject.objects.all()


class ProjectMemberRoleUpdateAPIView(UpdateAPIView):
    serializer_class = ProjectMemberRoleUpdateSerializer
    queryset = WorkspaceProject.objects.all()


class TaskListCreateAPIView(ListCreateAPIView):
    serializer_class = TaskListSerializer
    queryset = Task.objects.all()
    repo = TaskRepository

    def get_serializer_class(self):
        if self.request.method == 'POST' :
            self.serializer_class = TaskPostSerializer
        return super().get_serializer_class()
    
    def get_filter_methods(self):
        repo = self.repo()
        return {
            'project' : repo.get_by_project,
            'date' : repo.get_by_date,
            'share_date': repo.get_by_sharing_date
        }

    def get_queryset(self, **kwargs):
        filters = self.get_filter_methods()
        qs = Task.objects.all()
        for key, value in self.request.query_params.items():
            if key in filters:
                qs = filters[key](value, qs)
        return qs


class TaskRetriveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = TaskPostSerializer
    queryset = Task.objects.all()


class TaskCompletedAPIView(RetrieveUpdateAPIView):
    serializer_class = TaskCompletedSerializer
    queryset = Task.objects.all()


class TaskAddMemberAPIView(RetrieveUpdateAPIView):
    serializer_class = TaskAddMemberSerializer
    queryset = Task.objects.all()


class TaskMemberInviteView(UpdateAPIView):
    serializer_class = TaskMemberInvitationSerializer
    queryset = Task.objects.all()


class SubtaskListCreateAPIView(ListCreateAPIView):
    serializer_class = SubtaskListSerializer
    queryset = Subtask.objects.all().order_by('started_date')
    repo = SubtaskRepository

    def get_serializer_class(self):
        if self.request.method == 'POST' :
            self.serializer_class = SubtaskPostSerializer
        return super().get_serializer_class()
    
    def get_filter_methods(self):
        repo = self.repo()
        return {
            'task' : repo.get_by_task,
        }

    def get_queryset(self, **kwargs):
        filters = self.get_filter_methods()
        qs = Subtask.objects.all().order_by('started_date')
        for key, value in self.request.query_params.items():
            if key in filters:
                qs = filters[key](value, qs)
        return qs


class SubtaskRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = SubtaskPostSerializer
    queryset = Subtask.objects.all()


class SubtaskCompletedAPIView(RetrieveUpdateAPIView):
    serializer_class = SubtaskCompletedSerializer
    queryset = Subtask.objects.all()