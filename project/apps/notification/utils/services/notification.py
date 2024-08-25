from django.template import Template, Context
from django.utils.decorators import classonlymethod
from django.db.models import F
from asgiref.sync import sync_to_async
from ...models import NotificationType, UserNotificationSettings, SentNotification
from apps.bot.models.bot import Bot

class TemplateRenderer:
    """
    Renders notification content from templates.
    """
    @classonlymethod
    async def render(cls, template_string, context_data):
        template = Template(template_string)
        context = Context(context_data)
        return template.render(context)

class NotificationService:
    """
    Manages the process of sending notifications.
    """
    def __init__(self):
        self.channels = {}
        self.template_renderer = TemplateRenderer()

    def register_channel(self, name, channel_class):
        """
        Registers a new notification channel.
        """
        self.channels[name] = channel_class

    async def create_and_send_notifications_for_scheduled_post(self, schedule, status_message):
        """
        Creates and sends notifications for a scheduled post based on its status.
        """
        notification_type, _ = await sync_to_async(NotificationType.objects.get_or_create)(name='scheduled_post')

        user_channels = await sync_to_async(UserNotificationSettings.objects.filter)(
            user=schedule.post.user,
            notification_type=notification_type,
            is_active=True
        )

        user_channels = await sync_to_async(list)(user_channels)  # Convert QuerySet to list

        for user_channel in user_channels:
            channel = await self._get_channel(user_channel.channel.name)

            if channel:
                content = await self._create_notification_content(notification_type, schedule, status_message)

                # Determine recipient_id based on channel type
                if user_channel.channel.name == 'telegram':
                    recipient_id = user_channel.channel_settings.chat_id
                elif user_channel.channel.name == 'whatsapp':
                    recipient_id = user_channel.channel_settings.phone_number
                elif user_channel.channel.name == 'email':
                    recipient_id = user_channel.channel_settings.email_address

                await self._send_notification_and_log(channel, user_channel.user,
                                                       content, recipient_id,
                                                         notification_type)

    async def _get_channel_and_recipient(self, user_channel):
        """
        Gets the channel instance and recipient ID based on user notification settings.
        """
        if user_channel.channel.name == 'telegram':
            bot = await sync_to_async(Bot.objects.get)(user=user_channel.user, platform_type='telegram', is_active=True)
            channel = await self._get_channel('telegram', bot)
            recipient_id = user_channel.telegram_chat_id
        elif user_channel.channel.name == 'whatsapp':
            bot = await sync_to_async(Bot.objects.get)(user=user_channel.user, platform_type='whatsapp', is_active=True)
            channel = await self._get_channel('whatsapp', bot)
            recipient_id = user_channel.whatsapp_number
        elif user_channel.channel.name == 'email':
            channel = await self._get_channel('email')
            recipient_id = user_channel.email_address
        else:
            return None, None  # Invalid channel

        return channel, recipient_id

    async def _create_notification_content(self, notification_type, schedule, status_message):
        """
        Creates the notification content using the template.
        """
        context_data = {
            'post_content': schedule.post.content,
            'status_message': status_message,
        }
        return await self.template_renderer.render(notification_type.template, context_data)

    async def _send_notification_and_log(self, channel, user, content, recipient_id, notification_type):
        """
        Sends the notification and creates/updates the SentNotification record.
        """
        try:
            await sync_to_async(channel.send_notification)(user, content, recipient_id)
            await sync_to_async(SentNotification.objects.create)(
                user=user,
                notification_type=notification_type,
                channel=channel, 
                content=content,
                status='sent'
            )
        except Exception as e:
            await sync_to_async(SentNotification.objects.create)(
                user=user,
                notification_type=notification_type,
                channel=channel, 
                content=content,
                status='failed',
                error_message=str(e)
            )

    async def _get_channel(self, channel_name, bot=None):
        """
        Gets the appropriate channel class instance based on the channel name and bot information.
        """
        channel_class = self.channels.get(channel_name)
        if channel_class:
            if bot:
                return channel_class(bot)
            else:
                return channel_class()
        return None
