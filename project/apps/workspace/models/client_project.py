from django.db import models
from django.contrib.auth import get_user_model

from utils.models.base_model import BaseModel
from utils.slugify.custom_slugify import custom_slugify
from utils.text.truncate_content import truncate
from .workspace_project import WorkspaceProject

User = get_user_model()


class WorkspaceClientProject(BaseModel):
    title = models.CharField(
        'Proyektin adı',
        max_length=200
    )
    description = models.TextField(
        'Qısa təsvir',
        null=True, blank=True
    )
    workspace_project = models.ForeignKey(
        WorkspaceProject,
        on_delete=models.CASCADE,
        related_name='client_projects',
        verbose_name='Virtual ofis proyekti',
        null=True, blank=True
    )
    moderator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='clent_projects',
        verbose_name='Müştəri layihə rəhbəri',
        null=True, blank=True
    )
    slug = models.SlugField(
        "Link adı",
        help_text="Bu qismi boş buraxın. Avtomatik doldurulacaq.",
        null=True, blank=True        
    )

    class Meta:
        verbose_name='Müştərinin proyekti'
        verbose_name_plural='Müştərinin proyektləri'
        unique_together=['workspace_project', 'title']

    @property
    def truncated_description(self):
        return truncate(self.description)

    def save(self, *args, **kwargs):
        self.slug = custom_slugify(self.title)
        super(WorkspaceClientProject, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.workspace_project}=>{self.title}'