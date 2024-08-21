from django.db import models

from utils.models.base_model import BaseModel
from .workspace import Workspace

class WorkspaceInvitation(BaseModel):
    email = models.EmailField()
    token = models.CharField(max_length=32, unique=True)
    is_accepted = models.BooleanField(default=False)
    workspace = models.ForeignKey(
        Workspace, 
        related_name='invitations', 
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Virtual ofis üzv dəvəti'
        verbose_name_plural = 'Virtual ofis üzv dəvətləri'

    def __str__(self) -> str:
        return f'DəvətI:{self.workspace} üçün {self.email}-ə'