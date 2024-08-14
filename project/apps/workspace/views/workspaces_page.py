from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model

from ..models import (
    Workspace,
    WorkspaceCategory
)

User = get_user_model()

class WorkspacePageView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/workspaces/index.html'

    def get_context_data(self, **kwargs):
        context = super(WorkspacePageView, self).get_context_data(**kwargs)
        context["my_workspaces"] = Workspace.objects.filter(creator=self.request.user)
        context["workspace_categories"] = WorkspaceCategory.objects.all()
        # context["guest_workspaces"] = Workspace.objects.filter(workspace_users__user=self.request.user, workspace_users__is_creator = False)
        # context["users"] = User.objects.all()
        return context
    