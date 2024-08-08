from rest_framework.generics import (
    CreateAPIView,
    ListCreateAPIView, 
    ListAPIView,
    RetrieveUpdateDestroyAPIView
)

from .serializers import (
    WorkspaceListSerializer,
    WorkspacePostSerializer
)
from .repositories import WorkspaceRepository
from apps.workspace.models import Workspace


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