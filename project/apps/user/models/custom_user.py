from django.contrib.auth.models import AbstractUser
from django.db import models

import uuid

from utils.slugify.custom_slugify import custom_slugify
from utils.models.base_model import BaseModel
from apps.user.manager.custom_user_manager import CustomUserManager
    

class CustomUser(AbstractUser, BaseModel):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    slug = models.SlugField(
        "Link adı",
        help_text="Bu qismi boş buraxın. Avtomatik doldurulacaq.",
        null=True, blank=True        
    )
    is_banned = models.BooleanField(
        'Banned',
        default=False
    )
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, blank=True, null=True)

    objects = CustomUserManager()

    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'İstifadəçi'
        verbose_name_plural = 'İstifadəçilər'
    
    @property
    def full_name(self):
        if self.get_full_name():
            return self.get_full_name()
        else:
            return f'Admin User'
        
    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = custom_slugify(f'{self.full_name}{uuid.uuid4().hex[:6]}')
        super(CustomUser, self).save(*args, **kwargs)
