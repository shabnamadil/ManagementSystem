from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from ..models import (
    Workspace
)

class WorkspaceDetailView(DetailView, LoginRequiredMixin):
    queryset = Workspace.objects.filter(is_banned=False)
    template_name = 'pages/workspaces/components/workspace-detail.html'
    context_object_name = 'workspace'
