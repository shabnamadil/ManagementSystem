import telegram

from abc import ABC, abstractmethod
from django.core.mail import send_mail
from django.conf import settings

from apps.bot.models.bot import Bot
from utils.bots.telegram_bot.base_class import BaseTelegramBot
from utils.bots.whatsapp_bot.base_class import BaseWhatsAppBot
# from .base_whatsapp_bot import BaseWhatsAppBot

class NotificationChannel(ABC):
    """
    Defines an abstract base class for notification channels.
    """
    @abstractmethod
    def send_notification(self, user, content, recipient_id):
        """
        Sends a notification to the specified recipient.
        """
        pass

