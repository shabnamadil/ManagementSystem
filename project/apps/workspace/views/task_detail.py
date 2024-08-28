from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from ..models import (
    Task
)

class TaskDetailView(DetailView, LoginRequiredMixin):
    queryset = Task.objects.all()
    template_name = 'pages/workspaces/components/tasks/task-detail.html'
    context_object_name = 'task'
