from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

from utils.models.base_model import BaseModel
from utils.slugify.custom_slugify import custom_slugify
from utils.text.truncate_content import truncate
from utils.upload.task_image_upload import upload_to
from .workspace_project import WorkspaceProject

User = get_user_model()

class Task(BaseModel):
    PRIORITY_CHOICES = [
        ('Highest', 'Highest'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
        ('Lowest', 'Lowest')
    ]

    title = models.CharField(
        'Başlıq',
        max_length=200,
    )
    description = models.TextField(
        'Qısa təsvir',
        null=True, blank=True
    )
    content = models.TextField(
        verbose_name='Tapşırığın mətni'
    )
    file = models.FileField(
        null=True, blank=True,
        upload_to='tasks/'
    )
    ready_content = models.TextField(
        'Hazır mətn ',
        null=True, blank=True
    )
    priority = models.CharField(
        'Vaciblik dərəcəsi',
        max_length=30,
        choices=PRIORITY_CHOICES,
        default='PRIORITY_CHOICES[0][0]'
    )
    task_creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='project_tasks',
        verbose_name='Taskı əlavə etdi'
    )
    completed = models.BooleanField(default=False)
    project = models.ForeignKey(
        WorkspaceProject,
        on_delete=models.CASCADE,
        related_name='project_tasks',
        verbose_name='Layihə'
    )
    started = models.DateTimeField(
        'Tapşırığın başlama vaxtı'
    )
    deadline = models.DateTimeField(
        'Taskın bitmə tarixi'
    )
    sharing_date = models.DateTimeField(
        'Paylaşım tarixi',
        null=True, blank=True
    )
    slug = models.SlugField(
        "Link adı",
        help_text="Bu qismi boş buraxın. Avtomatik doldurulacaq.",
        null=True, blank=True        
    )

    class Meta:
        verbose_name = 'Tapşırıq'
        verbose_name_plural = 'Tapşırıqlar'
        unique_together = ['project', 'title']
        indexes = [models.Index(
            fields=['created', 'priority'],
        )]
        ordering = ('-created', 'priority')

    @property
    def truncated_content(self):
        return truncate(self.content)
    
    @property
    def started_date(self):
        return self.started.strftime('%m/%d/%Y, %H:%M')
    
    @property
    def deadline_date(self):
        return self.deadline.strftime('%d/%m/%Y, %H:%M')
    
    @property
    def completed_percent(self):
        if self.completed and self.subtasks.count() == 0:
            return 100
        elif self.completed == False and self.subtasks.count() == 0:
            return 0
        elif self.completed == False and self.subtasks.count() > 0:
            percent = 0
            count = self.subtasks.count()
            desired_percent = 100/count
            for task in self.subtasks.all():
                if task.completed:
                    percent += desired_percent
            return percent
        else:
            return 100
        

    def save(self, *args, **kwargs):
        self.slug = custom_slugify(self.title)
        super(Task, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.project}=>{self.title}' 
    
    def get_absolute_url(self):
        return reverse_lazy("task-detail", args=[self.id])