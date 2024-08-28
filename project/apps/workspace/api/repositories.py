from django.db.models import Q
from django.utils.dateparse import parse_date
from datetime import datetime

from apps.workspace.models import (
    Workspace,
    WorkspaceProject,
    Task,
    Subtask
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
    

class TaskRepository:
    DEFAULT_QS = Task.objects.all()
    
    def __init__(self):
        self.model = Task

    def get_by_project(self, project, qs=DEFAULT_QS):
        return qs.filter(Q(project__slug=project))
    
    def get_by_date(self, date, qs=DEFAULT_QS):
        try:
            # Assuming the incoming date is in 'YYYY-MM-DD' format
            parsed_date = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            return qs.none()  # or handle the error appropriately

        return qs.filter(Q(started__date__lte=parsed_date) & Q(deadline__date__gte=parsed_date))
    
    def get_by_sharing_date(self, date, qs=DEFAULT_QS):
        try:
            parsed_date = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            return qs.none()

        return qs.filter(sharing_date__date=parsed_date)
    

class SubtaskRepository:
    DEFAULT_QS = Subtask.objects.all()
    
    def __init__(self):
        self.model = Subtask

    def get_by_task(self, task, qs=DEFAULT_QS):
        return qs.filter(Q(task__slug=task))