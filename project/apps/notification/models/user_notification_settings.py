from django.db import models
from django.contrib.auth import get_user_model
from .notification_type import NotificationType
from .notification_channel import NotificationChannel

User = get_user_model()

class UserNotificationSettings(models.Model):
    """
    Kullanıcı bildirim tercihlerini saklar.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_type = models.ForeignKey(NotificationType, on_delete=models.CASCADE)
    channel = models.ForeignKey(NotificationChannel, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'notification_type', 'channel')
        indexes = [
            models.Index(fields=['user', 'notification_type']),
        ]