from django.db import models
from django.contrib.auth import get_user_model
from .notification_type import NotificationType
from .notification_channel import NotificationChannel
from utils.constants.choices import NOTIFICATION_STATUS_CHOICES

User = get_user_model()

class SentNotification(models.Model):
    """
    Gönderilen bildirimlerin ayrıntılarını saklar.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Bildirimi alan kullanıcı
    notification_type = models.ForeignKey(NotificationType, on_delete=models.CASCADE)  # Bildirim türü
    channel = models.ForeignKey(NotificationChannel, on_delete=models.CASCADE)  # Gönderim için kullanılan kanal
    content = models.TextField()  # Bildirim içeriği
    timestamp = models.DateTimeField(auto_now_add=True)  # Bildirimin gönderildiği zaman damgası
    status = models.CharField(max_length=20, choices=NOTIFICATION_STATUS_CHOICES, default='sent')  # Bildirimin durumu (gönderildi, iletildi, başarısız)
    error_message = models.TextField(blank=True, null=True)  # Hata mesajı (varsa)