from django.db import models

from utils.models.base_model import BaseModel
from .workspace_project import WorkspaceProject

class ProjectMemberInvitation(BaseModel):
    email = models.EmailField()
    token = models.CharField(max_length=32, unique=True)
    is_accepted = models.BooleanField(default=False)
    project = models.ForeignKey(
        WorkspaceProject, 
        related_name='invitations', 
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Layihə üzv dəvəti'
        verbose_name_plural = 'Layihə üzv dəvətləri'

    def __str__(self) -> str:
        return f'Dəvət:{self.project} üçün {self.email}-ə'