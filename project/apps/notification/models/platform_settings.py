from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class TelegramSettings(models.Model):
    """
    Telegram'a özgü bildirim ayarlarını saklar
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null = True)
    chat_id = models.CharField(max_length=255, null = True)  # chat_id artık null olamaz
    username = models.CharField(max_length=255, blank=True, null=True) 
    is_group_chat = models.BooleanField(default=False)
    group_chat_name = models.CharField(max_length=255, blank=True, null=True)

class WhatsAppSettings(models.Model):
    """
    WhatsApp'a özgü bildirim ayarlarını saklar
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null = True)
    phone_number = models.CharField(max_length=20, null = True)

class EmailSettings(models.Model):
    """
    E-postaya özgü bildirim ayarlarını saklar
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null = True)
    email_address = models.EmailField(null = True)