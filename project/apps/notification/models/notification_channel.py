from django.db import models
from utils.constants.choices import CHANNEL_CHOICES

class NotificationChannel(models.Model):
    """
    Mevcut bildirim kanallarını temsil eder (ör. Telegram, WhatsApp, Email).
    """
    name = models.CharField(max_length=50, choices=CHANNEL_CHOICES, unique=True)

    def __str__(self):
        return self.name