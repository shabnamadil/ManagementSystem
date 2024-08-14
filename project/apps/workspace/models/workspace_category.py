from django.db import models

from utils.models.base_model import BaseModel
from utils.slugify.custom_slugify import custom_slugify


class WorkspaceCategory(BaseModel):
    COLOR_CHOICES = [
        ("bg-danger", "red", ),
        ("bg-primary", "purple", ),
        ("bg-success", "green", ),
        ("bg-warning", "yellow", ),
        ("bg-light", "white", ),
        ("bg-dark", "black", ),
        ("bg-lightgreen", "lightgreen"),
        ("light-info-bg", "lightpink"),
        ("light-success-bg", "slightlygreen"),
        ("light-orange-bg", "lightorange"),
        ("bg-careys-pink", "pink"),
        ("bg-lightblue", "lightblue")
    ]
    
    name = models.CharField(
        'Kateqoriyanın adı', 
        max_length = 200, 
        unique = True
    )
    color = models.CharField(
        'Rəng',
        max_length=20,
        choices=COLOR_CHOICES
    )
    file = models.FileField(
        'Foto',
        upload_to='workspace-category/'
    )
    slug = models.SlugField(
        "Link adı",
        help_text="Bu qismi boş buraxın. Avtomatik doldurulacaq.",
        null=True, blank=True        
    )


    class Meta:
        verbose_name = 'Kateqoriya'
        verbose_name_plural = 'Kateqoriyalar'
        indexes = [models.Index(fields=['created'])]
        ordering = ('-created',)
        unique_together =['color', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = custom_slugify(self.name)
        super(WorkspaceCategory, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name