from django.db import models

from utils.models.base_model import BaseModel


class HowToWork(BaseModel):
    title = models.CharField(
        'Başlıq',
        max_length=200
    )
    description = models.TextField(
        'Qısa məlumat'
    )
    file = models.FileField(
        'Simvol',
        upload_to='home/how_to_work/'
    )

    class Meta:
        verbose_name = 'Necə işləyirik?'
        verbose_name_plural = 'Necə işləyirik?'
        indexes = [models.Index(fields=['created'])]
        ordering = ('-created',)

    def __str__(self) -> str:
        return self.title