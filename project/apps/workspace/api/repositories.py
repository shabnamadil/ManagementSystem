from django.db.models import Q

from apps.workspace.models import (
    Workspace,
    WorkspaceProject
)

class WorkspaceRepository:
    DEFAULT_QS = Workspace.objects.filter(is_banned=False).order_by('-created')
    
    def __init__(self):
        self.model = Workspace

    def get_by_creator(self, creator, qs=DEFAULT_QS):
        return qs.filter(Q(creator__slug=creator))
    

class WorkspaceProjectRepository:
    DEFAULT_QS = WorkspaceProject.objects.all()
    
    def __init__(self):
        self.model = WorkspaceProject

    def get_by_workspace(self, workspace, qs=DEFAULT_QS):
        return qs.filter(Q(workspace__slug=workspace))