from django.db import models
from django.contrib.auth import get_user_model

from utils.models.base_model import BaseModel
from . import Task

User = get_user_model()

class TaskAssignedMember(BaseModel):
    ROLE_CHOICES = [
        ('Adi üzv', 'Adi üzv'),
        ('Moderator', 'Moderator'),
        ('Admin', 'Admin'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='assigned_members',
        verbose_name='İstifadəçi'
    )
    role = models.CharField(
        'Tutduğu rol',
        max_length=20,
        choices=ROLE_CHOICES
    )
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='assigned_members',
        verbose_name='Task'
    )

    class Meta:
        verbose_name = 'Tapşırıq icraçısı'
        verbose_name_plural = 'Tapşırıq icraçıları'
        unique_together = ('user', 'task')

    def __str__(self) -> str:
        return f'{self.task} => {self.role} => {self.user}'