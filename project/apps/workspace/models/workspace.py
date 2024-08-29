from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

from utils.models.base_model import BaseModel
from utils.slugify.custom_slugify import custom_slugify
from utils.text.truncate_content import truncate
from .workspace_category import WorkspaceCategory

User = get_user_model()


class Workspace(BaseModel):
    WORKSPACE_STATUS_CHOICES = [
        ('Şəxsi', 'Şəxsi'),
        ('Hər kəsə açıq', 'Hər kəsə açıq'),
    ]
    
    title = models.CharField(
        'Virtual ofisin adı', 
        max_length = 20, 
        unique = True
    )
    description = models.TextField(
        'Qısa təsvir',
        null = True, 
        blank = True
    )
    category = models.ForeignKey(
        WorkspaceCategory,
        on_delete=models.CASCADE, 
        related_name='workspaces',
        verbose_name='Kateqoriya'
    )
    status = models.CharField(
        choices=WORKSPACE_STATUS_CHOICES,
        max_length=15,
        default='Şəxsi'
    )
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='creator_workspaces',
        verbose_name='Virtual ofis yaratdı'
    )
    slug = models.SlugField(
        "Link adı",
        help_text="Bu qismi boş buraxın. Avtomatik doldurulacaq.",
        null=True, blank=True        
    )
    is_banned = models.BooleanField(
        'Banned',
        default=False)


    class Meta:
        verbose_name = 'Virtual ofis'
        verbose_name_plural = 'Virtual ofis'
        indexes = [models.Index(fields=['created'])]
        ordering = ('-created',)

    @property
    def truncated_description(self):
        return truncate(self.description)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = custom_slugify(self.title)
        super(Workspace, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse_lazy("workspace-detail", args=[self.id])

    def __str__(self) -> str:
        return self.title