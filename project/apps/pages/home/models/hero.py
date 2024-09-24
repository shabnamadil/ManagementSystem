from django.db import models

from utils.models.singleton import SingletonModel
from utils.models.base_model import BaseModel


class HeroSection(SingletonModel, BaseModel):
    title = models.CharField(
        'Başlıq',
        max_length=200
    )
    description = models.TextField(
        'Qısa məlumat'
    )
    image = models.FileField(
        upload_to='home/hero/'
    )

    class Meta:
        verbose_name = 'Ana səhifə birinci bölüm'
        verbose_name_plural = 'Ana səhifə birinci bölüm'

    def __str__(self) -> str:
        return f'Ana səhifə birinci bölüm məlumatları'