from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from ..models import (
    WorkspaceProject
)

class ProjectDetailView(DetailView, LoginRequiredMixin):
    queryset = WorkspaceProject.objects.all()
    template_name = 'pages/workspaces/components/projects/project-detail.html'
    context_object_name = 'project'
