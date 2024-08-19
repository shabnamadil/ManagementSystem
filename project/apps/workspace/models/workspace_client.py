from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from utils.models.base_model import BaseModel
from utils.slugify.custom_slugify import custom_slugify
from utils.upload.workspace_client_image_upload import upload_to

User = get_user_model()


class WorkspaceClient(BaseModel):
    full_name = models.CharField(
        'Ad, soyad',
        max_length=100
    )
    email = models.EmailField(
        'Email',
        unique=True
    )
    image = models.ImageField(
        'Foto',
        null=True, blank=True,
        upload_to=upload_to
    )
    company = models.CharField(
        'Şirkət',
        max_length=200,
        null=True, blank=True
    )
    profession = models.CharField(
        'Peşə',
        max_length=200,
        null=True, blank=True
    )
    description = models.TextField(
        'Haqqında',
        null=True, blank=True
    )
    phone_number = models.CharField(
        'Əlaqə nömrəsi',
        max_length=20, 
        help_text='Only numeric values allowed', 
        null=True, blank=True
    )
    facebook_link = models.URLField(
        'Facebook hesabı',
        null=True, blank=True
    )
    instagram_link = models.URLField(
        'Instagram hesabı',
        null=True, blank=True
    )
    slug = models.SlugField(
        "Link adı",
        help_text="Bu qismi boş buraxın. Avtomatik doldurulacaq.",
        null=True, blank=True        
    )

    class Meta:
        verbose_name = 'Virtual ofis müştərisi'
        verbose_name_plural = 'Virtual ofis müştəriləri'

    def save(self, *args, **kwargs):
        self.slug = custom_slugify(self.full_name)
        super(WorkspaceClient, self).save(*args, **kwargs)

    def clean(self) -> str:
        super().clean()
        phone_number = self.phone_number
        if phone_number and not phone_number.isdigit():
            raise ValidationError('Only numeric values are allowed for phone number.')
        if phone_number and len(phone_number) < 10:
            raise ValidationError('Phone number must be at least 10 characters')
        return phone_number
    
    def __str__(self) -> str:
        return self.full_name