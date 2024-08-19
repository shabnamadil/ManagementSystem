from django.db import models
from django.contrib.auth import get_user_model

from utils.models.base_model import BaseModel
from ..models import Workspace

User = get_user_model()

class WorkspaceMember(BaseModel):
    ROLE_CHOICES = [
        ('Adi üzv', 'Adi üzv'),
        ('Moderator', 'Moderator'),
        ('Admin', 'Admin'),
        ('Super admin', 'Super admin')
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='workspace_members',
        verbose_name='İstifadəçi'
    )
    role = models.CharField(
        'Tutduğu rol',
        max_length=20,
        choices=ROLE_CHOICES
    )
    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
        related_name='workspace_members',
        verbose_name='Virtual ofis'
    )

    class Meta:
        verbose_name = 'Virtual ofis üzvü'
        verbose_name_plural = 'Virtual ofis üzvləri'
        unique_together = ('user', 'workspace')

    def __str__(self) -> str:
        return f'{self.workspace} => {self.role} => {self.user}'