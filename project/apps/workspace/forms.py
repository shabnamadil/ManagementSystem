from django import forms
from django.core.exceptions import ValidationError

from apps.workspace.models import (
    Workspace,
    WorkspaceProject,
    WorkspaceClientProject,
    Task
)

class WorkspaceForm(forms.ModelForm):
    class Meta:
        model = Workspace
        fields = (
            'id',
            'title', 
            'description',
            'members', 
            'admins',
            'super_admin',
            'status',
            'is_banned',
            'creator',
            'slug'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        admins = cleaned_data.get('admins', [])
        members = cleaned_data.get('members', [])
        super_admin = cleaned_data.get('super_admin', None)

        if not set(admins).issubset(set(members)):
            raise ValidationError('All admins must be member of workspace')
        if super_admin and super_admin not in admins:
            raise ValidationError('Super admin must be one of the admins')

        return cleaned_data


class WorkspaceProjectForm(forms.ModelForm):
    class Meta:
        model = WorkspaceProject
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        workspace = cleaned_data.get('workspace', None)
        moderator = cleaned_data.get('moderator', None)

        if moderator not in workspace.members.all():
            raise ValidationError('Moderator must be member of Workspace')


class WorkspaceClientProjectForm(forms.ModelForm):
    class Meta:
        model = WorkspaceClientProject
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        workspace_project = cleaned_data.get('workspace_project', None)
        moderator = cleaned_data.get('moderator', None)

        if moderator not in workspace_project.workspace.members.all():
            raise ValidationError('Moderator must be member of Workspace')


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        project = cleaned_data.get('project', None)
        task_assigned_to = cleaned_data.get('task_assigned_to', None)

        for user in task_assigned_to:
            if user not in project.workspace_project.workspace.members.all():
                raise ValidationError('Task can only be assigned to workspace members ')
