from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

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
        return self._get_username_from_url(self.instagram_link, "https://www.instagram.com/")

    @property
    def facebook_username(self):
        return self._get_username_from_url(self.facebook_link, "https://www.facebook.com/")

    @property
    def tiktok_username(self):
        return self._get_username_from_url(self.tiktok_link, "https://www.tiktok.com/")

    @property
    def youtube_username(self):
        return self._get_username_from_url(self.youtube_link, "https://www.youtube.com/")

    def _get_username_from_url(self, url, platform_base_url):
        if not url or not url.startswith(platform_base_url):
            return None

        from urllib.parse import urlparse
        parsed_url = urlparse(url)
        path_parts = parsed_url.path.split('/')

        if len(path_parts) > 1:
            return path_parts[-1]

        return None