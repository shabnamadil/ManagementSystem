from django.db import models
from django.contrib.auth import get_user_model

from utils.models.base_model import BaseModel
from utils.slugify.custom_slugify import custom_slugify
from utils.text.truncate_content import truncate
from utils.upload.task_image_upload import upload_to
from .project_task import Task

User = get_user_model()

class Subtask(BaseModel):
    job = models.TextField(
        'Görülməli olan iş',
    )
    subtask_creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subtasks',
        verbose_name='Subtaskı əlavə etdi'
    )
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='subtasks',
        verbose_name='Tapşırq'
    )
    assigned_to = models.ForeignKey(
        'workspace.TaskAssignedMember',
        on_delete=models.CASCADE,
        related_name='subtask',
        null=True, blank=True
    )
    started_date = models.DateTimeField(
        'Subtaskın başlama vaxtı'
    )
    deadline = models.DateTimeField(
        'Subtaskın bitmə tarixi'
    )
    content = models.TextField(
        verbose_name='Hazır Mətn',
        null=True, blank=True
    )
    file = models.FileField(
        null=True, blank=True,
        upload_to='subtasks'
    )
    completed = models.BooleanField(
        default=False
    )
    slug = models.SlugField(
        "Link adı",
        help_text="Bu qismi boş buraxın. Avtomatik doldurulacaq.",
        null=True, blank=True        
    )

    class Meta:
        verbose_name = 'Subtasks'
        verbose_name_plural = 'Subtasks'
        unique_together = ['task', 'job']
        indexes = [models.Index(
            fields = ['created']
        )]
        ordering = ('-created',)

    @property
    def truncated_content(self):
        return truncate(self.content)

    def save(self, *args, **kwargs):
        self.slug = custom_slugify(self.job)
        super(Subtask, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.task}' 

