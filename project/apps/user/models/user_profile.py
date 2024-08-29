from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from urllib.parse import urlparse

from utils.upload.workspace_client_image_upload import upload_to
from utils.models.base_model import BaseModel

User = get_user_model()


class Profile(BaseModel):
    image = models.ImageField(
        'Foto',
        null=True, blank=True,
        upload_to=upload_to
    )
    profession = models.CharField(
        max_length=255, 
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
    tiktok_link = models.URLField(
        'Tiktok hesabı',
        null=True, blank=True
    )
    youtube_link = models.URLField(
        'Youtube hesabı',
        null=True, blank=True
    )
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, 
        related_name="user_profile",
        verbose_name='İstifadəçi profili'
    )


    class Meta:
        verbose_name = 'İstifadəçi profili'
        verbose_name_plural = 'İstifadəçi profilləri'

    def clean(self) -> str:
        super().clean()
        phone_number = self.phone_number
        if phone_number and not phone_number.isdigit():
            raise ValidationError('Only numeric values are allowed for phone number.')
        if phone_number and len(phone_number) < 10:
            raise ValidationError('Phone number must be at least 10 characters')
        return phone_number
    

    def __str__(self) -> str:
        return f'{self.user}  profile'
    
    @property
    def instagram_username(self):
        if self.instagram_link:
            parsed_url = urlparse(self.instagram_link)
            # Assuming the URL format is something like 'https://www.instagram.com/username/'
            path_segments = parsed_url.path.strip('/').split('/')
            if path_segments:
                return path_segments[0]
        return None
  