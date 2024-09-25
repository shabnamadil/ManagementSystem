from django.db import models

from utils.models.base_model import BaseModel


class Statistics(BaseModel):
    title = models.CharField(
        'Başlıq',
        max_length=200
    )
    number = models.IntegerField(
        'Miqdar'
    )
    file = models.FileField(
        'Simvol',
        upload_to='home/statistics/'
    )

    class Meta:
        verbose_name = 'Stastika'
        verbose_name_plural = 'Statistikalar'
        indexes = [models.Index(fields=['created'])]
        ordering = ('-created',)

    def __str__(self) -> str:
        return self.title