from django.core.management.base import BaseCommand

# from apps.reserve.telegram_bot.example.car_info_bot import CarInfoBot
from apps.reserve.telegram_bot.example.ai_bot import AIChatBot

class Command(BaseCommand):
    help = 'Start the CarInfoBot'

    def handle(self, *args, **kwargs):
        bot = AIChatBot()
        bot.run()