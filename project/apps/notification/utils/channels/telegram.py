import telegram

from utils.bots.telegram_bot.base_class import BaseTelegramBot

from .base import NotificationChannel

class TelegramChannel(NotificationChannel):
    """
    Sends notifications via Telegram.
    """
    def __init__(self, telegram_bot):
        self.bot = BaseTelegramBot(token=telegram_bot.token)

    async def send_notification(self, user, content, chat_id):
        """
        Sends a Telegram notification.
        """
        try:
            await self.bot.send_message(chat_id=chat_id, text=content)
        except telegram.error.TelegramError as e:
            # Error handling - log or perform other actions as needed
            print(f"Telegram sending error: {e}")

