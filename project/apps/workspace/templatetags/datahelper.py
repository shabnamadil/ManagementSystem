from django import template
from ..models.workspace import Workspace

register = template.Library()


@register.filter
def is_workspace_moderator(workspace, request):
    return workspace in Workspace.objects.filter(workspace_users__user=request.user, workspace_users__is_moderator = True)

@register.filter
def is_workspace_creator(workspace, request):
    return workspace in Workspace.objects.filter(workspace_users__user=request.user, workspace_users__is_creator = True)