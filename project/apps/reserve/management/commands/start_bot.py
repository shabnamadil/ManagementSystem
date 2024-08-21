from django.core.management.base import BaseCommand

from apps.reserve.utils.telegram_bot.reserve_bot import ReserveBot
from apps.notification.models import Bot

import multiprocessing

def start_bot(bot):
    reserve_bot = ReserveBot(bot=bot)
    reserve_bot.run()

class Command(BaseCommand):
    help = 'Start the ReserveBot'

    def handle(self, *args, **kwargs):
        bots = Bot.objects.filter(is_active=True)
        processes = []

        for bot in bots:
            p = multiprocessing.Process(target=start_bot, args=(bot,))
            p.start()
            processes.append(p)

        for p in processes:
            p.join()