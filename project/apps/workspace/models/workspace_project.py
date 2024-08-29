from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

from .workspace import Workspace
from utils.models.base_model import BaseModel
from utils.slugify.custom_slugify import custom_slugify
from utils.text.truncate_content import truncate

User = get_user_model()


class WorkspaceProject(BaseModel):
    title = models.CharField(
        'Layihənin adı',
        max_length=200
    )
    description = models.TextField(
        'Qısa təsvir',
        null = True, 
        blank = True
    )
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='workspace_projects',
        verbose_name='Layihəni yaratdı'
    )
    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
        related_name='workspace_projects',
        verbose_name='Virtual ofis'
    )
    slug = models.SlugField(
        "Link adı",
        help_text="Bu qismi boş buraxın. Avtomatik doldurulacaq.",
        null=True, blank=True        
    )

    class Meta:
        verbose_name='Layihə'
        verbose_name_plural='Layihələr'
        indexes = [models.Index(fields=['created'])]
        ordering = ('-created',)

    @property
    def truncated_description(self):
        return truncate(self.description)
    
    @property
    def workspace_and_project_members(self):
        # Using a set to ensure uniqueness of members
        members = set()

        # Adding workspace members
        if self.workspace.workspace_members.exists():
            for member in self.workspace.workspace_members.all():
                members.add(member.user)

        # Adding project members
        if self.project_members.exists():
            for member in self.project_members.all():
                if member not in members:
                    members.add(member.user)
        return list(members)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = custom_slugify(self.title)
        super(WorkspaceProject, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse_lazy("project-detail", args=[self.id])

    def __str__(self) -> str:
        return self.title