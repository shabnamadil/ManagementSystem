from django.db import models

from utils.models.base_model import BaseModel
from .project_task import Task

class TaskInvitation(BaseModel):
    email = models.EmailField()
    token = models.CharField(max_length=32, unique=True)
    is_accepted = models.BooleanField(default=False)
    task = models.ForeignKey(
        Task, 
        related_name='invitations', 
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Tasküzv dəvəti'
        verbose_name_plural = 'Task üzv dəvətləri'

    def __str__(self) -> str:
        return f'DəvətI:{self.task} üçün {self.email}-ə'