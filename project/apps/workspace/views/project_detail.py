from typing import Any
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from ..models import (
    WorkspaceProject,
    Task
)

class ProjectDetailView(DetailView, LoginRequiredMixin):
    queryset = WorkspaceProject.objects.all()
    template_name = 'pages/workspaces/components/projects/project-detail.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        cx = super().get_context_data(**kwargs)
        request_user = self.request.user 
        cx['sent_tasks'] = Task.objects.filter(task_sent_to__user=request_user)
        return cx
