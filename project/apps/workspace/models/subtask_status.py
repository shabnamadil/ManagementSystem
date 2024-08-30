from django.db import models
from django.contrib.auth import get_user_model

from utils.models.base_model import BaseModel
from .subtask import Subtask

User = get_user_model()

class SubtaskStatus(BaseModel):
    STATUS_CHOICES = [
        ('In progress', 'In progress'),
        ('Accepted', 'Accepted')
    ]
    status_name = models.CharField(
        'Subtaskın statusu',
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_CHOICES[0][1]
    )
    note = models.TextField(
        'Qeyd',
        null=True, blank=True
    )
    subtask = models.OneToOneField(
        Subtask,
        on_delete=models.CASCADE,
        related_name='status'
    )
    

    class Meta:
        verbose_name = 'Subtask statusu'
        verbose_name_plural = 'Subtask statusları'
        unique_together = ['subtask', 'status_name']

    def __str__(self) -> str:
        return f'{self.subtask} => {self.status_name} => {self.id}' 

