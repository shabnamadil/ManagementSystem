from rest_framework.generics import (
    CreateAPIView,
    ListCreateAPIView, 
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
    UpdateAPIView
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
    ProjectPostSerializer
)

from .repositories import WorkspaceRepository
from apps.workspace.models import (
    Workspace,
    WorkspaceCategory,
    WorkspaceProject
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

    def get_serializer_class(self):
        if self.request.method == 'POST' :
            self.serializer_class = ProjectPostSerializer
        return super().get_serializer_class()


class ProjectRetrieveUpdateDestoryAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectPostSerializer
    queryset = WorkspaceProject.objects.all()