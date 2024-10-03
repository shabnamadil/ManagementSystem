from django.db import models

from utils.models.base_model import BaseModel


class BlogCategory(BaseModel):
    category_name = models.CharField(
        'Kateqoriya adı', 
        max_length=150
    )

    class Meta:
        verbose_name = ('Bloq kateqoriyası')
        verbose_name_plural = ('Bloq kateqoriyaları')

    def __str__(self) -> str:
        return self.category_name