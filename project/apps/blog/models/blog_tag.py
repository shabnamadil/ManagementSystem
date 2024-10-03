from django.db import models

from utils.models.base_model import BaseModel


class BlogTag(BaseModel):
    tag_name = models.CharField(
        'Tag', 
        max_length=150
    )

    class Meta:
        verbose_name = ('Bloq teqi')
        verbose_name_plural = ('Bloq teqləri')

    def __str__(self) -> str:
        return self.tag_name