# apps/reserve/signals.py

import multiprocessing
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from apps.bot.models import Bot
from .utils.bots.reserve_bot import ReserveBot

# Store running bot processes
running_bots = {}

def start_bot(bot):
    reserve_bot = ReserveBot(bot=bot)
    reserve_bot.run()

def stop_bot(bot_id):
    if bot_id in running_bots:
        running_bots[bot_id].terminate()
        running_bots[bot_id].join()
        del running_bots[bot_id]

@receiver(post_save, sender=Bot)
def handle_bot_save(sender, instance, **kwargs):
    """Start or restart a bot when the Bot model is saved."""
    if instance.is_active:
        if instance.id in running_bots:
            stop_bot(instance.id)  # Restart the bot if it's already running
        p = multiprocessing.Process(target=start_bot, args=(instance,))
        p.start()
        running_bots[instance.id] = p
        print(f'Started or restarted bot: {instance.name}')
    else:
        # Stop the bot if it's marked inactive
        if instance.id in running_bots:
            stop_bot(instance.id)
            print(f'Stopped bot with ID: {instance.id}')

@receiver(post_delete, sender=Bot)
def handle_bot_delete(sender, instance, **kwargs):
    """Stop a bot when the Bot model is deleted."""
    stop_bot(instance.id)
    print(f'Stopped bot with ID: {instance.id} because it was deleted.')
