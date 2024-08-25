from django.db import models
from django.contrib.auth import get_user_model

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from utils.constants.choices import NOTIFICATION_TYPE_CHOICES, CHANNEL_CHOICES, NOTIFICATION_STATUS_CHOICES

User = get_user_model()


class NotificationType(models.Model):
    """
    Represents different types of notifications (e.g., scheduled post, new follower).
    """
    name = models.CharField(
        max_length=50, 
        choices=NOTIFICATION_TYPE_CHOICES, 
        unique=True
    )
    template = models.TextField()  # Template for notification content

    def __str__(self):
        return self.name
    
class NotificationChannel(models.Model):
    """
    Represents available notification channels (e.g., Telegram, WhatsApp, Email).
    """
    name = models.CharField(max_length=50, choices=CHANNEL_CHOICES, unique=True)

    def __str__(self):
        return self.name

class UserNotificationSettings(models.Model):
    """
    Stores user notification preferences.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    notification_type = models.ForeignKey(NotificationType, on_delete=models.CASCADE) 
    channel = models.ForeignKey(NotificationChannel, on_delete=models.CASCADE) 
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null = True)  # GenericForeignKey için
    object_id = models.PositiveIntegerField(null = True)  # GenericForeignKey için
    channel_settings = GenericForeignKey('content_type', 'object_id')  # Kanal özel ayarları
    is_active = models.BooleanField(default=True) 

    class Meta:
        unique_together = ('user', 'notification_type', 'channel')
        indexes = [
            models.Index(fields=['user', 'notification_type']),
        ]

# Kanal özel ayar modellerini tanımlayın
class TelegramSettings(models.Model):
    """
    Stores Telegram-specific notification settings.
    """
    chat_id = models.CharField(max_length=255, blank=True, null=True)  
    username = models.CharField(max_length=255, blank=True, null=True)  # New field for Telegram username
    is_group_chat = models.BooleanField(default=False) 
    group_chat_name = models.CharField(max_length=255, blank=True, null=True)  

class WhatsAppSettings(models.Model):
    """
    Stores WhatsApp-specific notification settings.
    """
    phone_number = models.CharField(max_length=20, blank=True, null=True) 

class EmailSettings(models.Model):
    """
    Stores email-specific notification settings.
    """
    email_address = models.EmailField(blank=True, null=True)


class SentNotification(models.Model):
    """
    Stores details of sent notifications.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User who received the notification
    notification_type = models.ForeignKey(NotificationType, on_delete=models.CASCADE)  # Type of notification
    channel = models.ForeignKey(NotificationChannel, on_delete=models.CASCADE)  # Channel used for sending
    content = models.TextField()  # Notification content
    timestamp = models.DateTimeField(auto_now_add=True)  # Timestamp of when the notification was sent
    status = models.CharField(max_length=20, choices=NOTIFICATION_STATUS_CHOICES, default='sent')  # Status of the notification (sent, delivered, failed)
    error_message = models.TextField(blank=True, null=True)  # Error message (if any)