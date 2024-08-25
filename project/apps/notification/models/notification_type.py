from django.db import models
from utils.constants.choices import NOTIFICATION_TYPE_CHOICES

class NotificationType(models.Model):
    """
    Farklı bildirim türlerini temsil eder (ör. planlanmış gönderi, yeni takipçi).
    """
    name = models.CharField(max_length=50, choices=NOTIFICATION_TYPE_CHOICES, unique=True)
    template = models.TextField()  # Bildirim içeriği için şablon

    def __str__(self):
        return self.name