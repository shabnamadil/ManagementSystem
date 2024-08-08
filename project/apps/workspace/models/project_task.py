from django.db import models
from django.contrib.auth import get_user_model

from ckeditor_uploader.fields import RichTextUploadingField

from utils.models.base_model import BaseModel
from utils.slugify.custom_slugify import custom_slugify
from utils.text.truncate_content import truncate
from utils.upload.task_image_upload import upload_to
from .client_project import WorkspaceClientProject

User = get_user_model()

class Task(BaseModel):
    title = models.CharField(
        'Başlıq',
        max_length=200,
    )
    content = RichTextUploadingField(
        null=True, blank=True,
        verbose_name='Tapşırığın mətni'
    )
    file = models.FileField(
        null=True, blank=True,
        upload_to=upload_to
    )
    task_creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='client_project_tasks',
        verbose_name='Taskı əlavə etdi'
    )
    task_assigned_to = models.ManyToManyField(
        User,
        related_name='project_tasks',
        verbose_name='Taskı yerinə yetirməlidir'
    )
    project = models.ForeignKey(
        WorkspaceClientProject,
        on_delete=models.CASCADE,
        related_name='project_tasks',
        verbose_name='Müştəri layihəsi'
    )
    deadline = models.DateTimeField(
        'Taskın bitmə tarixi'
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

    @property
    def truncated_content(self):
        return truncate(self.content)

    def save(self, *args, **kwargs):
        self.slug = custom_slugify(self.title)
        super(Task, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.project}=>{self.title}' 

