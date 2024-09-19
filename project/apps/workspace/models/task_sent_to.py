from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

from utils.models.base_model import BaseModel
from .project_task import Task

User = get_user_model()

class TaskSentTo(BaseModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='task_sent_to',
        verbose_name='User'
    )
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='task_sent_to',
        verbose_name='Task'
    )

    class Meta:
        unique_together = ['user', 'task']

    def __str__(self) -> str:
        return f'{self.task}=>{self.user} - ə göndərildi' 