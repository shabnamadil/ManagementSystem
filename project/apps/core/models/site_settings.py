from django.db import models
from utils.models.base_model import BaseModel
from utils.models.singleton import SingletonModel

class SiteSettings(BaseModel, SingletonModel):
    site_name = models.CharField(max_length=255, verbose_name="Site Name")
    logo = models.ImageField(upload_to='logos/', verbose_name="Site Logo")
    favicon = models.ImageField(upload_to='favicons/', verbose_name="Favicon")
    location = models.CharField(
        'Məkan',
        max_length=200
    )
    number = models.CharField(
        'Əlaqə nömrəsi',
        max_length=20
    )
    email = models.EmailField(
        'Email ünvanı'
    )
    facebook = models.URLField(
        'Facebook hesab linki',
        null=True, blank=True
    )
    youtube = models.URLField(
        'Youtube hesab linki',
        null=True, blank=True
    )
    instagram = models.URLField(
        'Instagram hesab linki',
        null=True, blank=True
    )
    linkedin = models.URLField(
        'Linkedin hesab linki',
        null=True, blank=True
    )
    tiktok = models.URLField(
        'Tiktok hesab linki',
        null=True, blank=True
    )
    footer_title = models.CharField(
        "Footer title", 
        max_length=200
    )
    footer_description = models.TextField(
        'Footer description'
    )
    footer_image = models.ImageField(
        'Footer image',
        upload_to='footer'
    )
    
    class Meta:
        verbose_name = "Site Setting"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return self.site_name
