from django.contrib import admin
from .models import (
    NotificationType,
    NotificationChannel,
    UserNotificationSettings,
    SentNotification,
    TelegramSettings,
)

class UserNotificationSettingsAdmin(admin.ModelAdmin):
    list_display = ('user', 'notification_type', 'channel', 'is_active')
    list_filter = ('notification_type', 'channel', 'is_active')
    search_fields = ('user__username', 'notification_type__name', 'channel__name')

class SentNotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'notification_type', 'channel', 'status', 'timestamp')
    list_filter = ('notification_type', 'channel', 'status', 'timestamp')
    search_fields = ('user__username', 'notification_type__name', 'channel__name', 'status')

class NotificationTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class NotificationChannelAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(TelegramSettings)
admin.site.register(NotificationType, NotificationTypeAdmin)
admin.site.register(NotificationChannel, NotificationChannelAdmin)
admin.site.register(UserNotificationSettings, UserNotificationSettingsAdmin)
admin.site.register(SentNotification, SentNotificationAdmin)