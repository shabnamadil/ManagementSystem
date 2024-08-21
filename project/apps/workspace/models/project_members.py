from django.db import models
from django.contrib.auth import get_user_model

from utils.models.base_model import BaseModel
from . import WorkspaceProject

User = get_user_model()

class ProjectMember(BaseModel):
    ROLE_CHOICES = [
        ('Adi üzv', 'Adi üzv'),
        ('Moderator', 'Moderator'),
        ('Admin', 'Admin'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='project_members',
        verbose_name='İstifadəçi'
    )
    role = models.CharField(
        'Tutduğu rol',
        max_length=20,
        choices=ROLE_CHOICES
    )
    project = models.ForeignKey(
        WorkspaceProject,
        on_delete=models.CASCADE,
        related_name='project_members',
        verbose_name='Layihə'
    )

    class Meta:
        verbose_name = 'Layihə üzvü'
        verbose_name_plural = 'Layihə üzvləri'
        unique_together = ('user', 'project')

    def __str__(self) -> str:
        return f'{self.project} => {self.role} => {self.user}'