from django.db import models

from utils.models.base_model import BaseModel
from utils.slugify.custom_slugify import custom_slugify


class FreelancerCategory(BaseModel):
    name = models.CharField(
        'Kateqoriyanın adı', 
        max_length = 200, 
        unique = True
    )
    file = models.FileField(
        'Kateqoriya simvolu',
        upload_to='freelancer-category/'
    )
    small_description = models.CharField(
        'Kiçik izahat',
        max_length=250
    )
    large_description = models.TextField(
        'Kateqoriya haqqında məlumat',
        help_text='Bura geniş məlumat əlavə edilir.'
    )
    slug = models.SlugField(
        "Link adı",
        help_text="Bu qismi boş buraxın. Avtomatik doldurulacaq.",
        null=True, blank=True        
    )


    class Meta:
        verbose_name = 'Frilanser kateqoriya'
        verbose_name_plural = 'Frilanser kateqoriyaları'
        indexes = [models.Index(fields=['created'])]
        ordering = ('-created',)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = custom_slugify(self.name)
        super(FreelancerCategory, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name