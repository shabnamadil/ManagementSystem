from utils.bots.whatsapp_bot.base_class import BaseWhatsAppBot
from .base import NotificationChannel

class WhatsAppChannel(NotificationChannel):
    """
    Sends notifications via WhatsApp.
    """
    def __init__(self, whatsapp_bot):
        self.bot = BaseWhatsAppBot(
            account_sid=whatsapp_bot.credentials['account_sid'],
            auth_token=whatsapp_bot.credentials['auth_token'],
            from_phone_number=whatsapp_bot.credentials['from_phone_number']
        )

    async def send_notification(self, user, content, to_phone_number):
        """
        Sends a WhatsApp notification.
        """
        try:
            await self.bot.send_message(to_phone_number, content)
        except Exception as e:
            # Error handling - log or perform other actions as needed
            print(f"WhatsApp sending error: {e}")

