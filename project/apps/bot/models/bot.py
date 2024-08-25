from django.db import models
from django.contrib.auth import get_user_model
from utils.constants.choices import PLATFORM_TYPE_CHOICES

User = get_user_model()

class Bot(models.Model):
    """
    Represents bots for users on different platforms.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # The user who owns the bot
    name = models.CharField(max_length=100, null=False, blank=False)  # Bot's name
    platform_type = models.CharField(max_length=20, choices=PLATFORM_TYPE_CHOICES)  # Platform type (Telegram, WhatsApp, Email)
    token = models.CharField(max_length=255)  # API token for the platform
    is_active = models.BooleanField(default=True)  # Whether the bot is active or not

    class Meta:
        unique_together = ('user', 'platform_type')  # A user cannot have multiple active bots on the same platform