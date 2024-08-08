from django.db import models
from django.contrib.auth import get_user_model

from utils.models.base_model import BaseModel
from .workspace import Workspace

User = get_user_model()


class WorkspaceProject(BaseModel):
    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
        related_name='workspace_projects',
        verbose_name='Virtual ofis'
    )
    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='client_workspace_projects',
        verbose_name='Müştəri'
    )
    moderator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='workspace_projects',
        verbose_name='Virtual ofis layihə moderatoru',
        null=True, blank=True
    )

    class Meta:
        verbose_name='Virtual ofis layihəsi'
        verbose_name_plural='Virtual ofis layihələri'
        unique_together = ['workspace', 'client']

    def __str__(self) -> str:
        return f'{self.workspace}=>{self.client}'