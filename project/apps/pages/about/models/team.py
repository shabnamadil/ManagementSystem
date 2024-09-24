from django.db import models

from utils.models.base_model import BaseModel


class Team(BaseModel):
    full_name = models.CharField(
        'Ad, Soyad',
        max_length=200
    )
    profession = models.CharField(
        'Peşə',
        max_length=200
    )
    image = models.ImageField(
        'Foto',
        upload_to='team'
    )
    twitter = models.URLField(
        'Twitter hesab linki',
        null=True, blank=True
    )
    facebook = models.URLField(
        'Facebook hesab linki',
        null=True, blank=True
    )
    github = models.URLField(
        'Github hesab linki',
        null=True, blank=True
    )

    class Meta:
        verbose_name = 'Komanda üzvü'
        verbose_name_plural = 'Komanda üzvləri'

    def __str__(self) -> str:
        return self.full_name