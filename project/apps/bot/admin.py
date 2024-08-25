from django.contrib import admin
from .models import Bot, Chat, Message, Media

class ChatInline(admin.TabularInline):
    model = Chat
    extra = 0
    show_change_link = True  # Chat'e tıklandığında detay sayfasına yönlendirmek için
    readonly_fields = ('chat_id', 'username', 'first_name', 'last_name', 'chat_type', 'title', 'is_active', 'joined_at', 'last_interaction')

class MediaInline(admin.TabularInline):
    model = Media
    extra = 0
    readonly_fields = ('file_size', 'duration', 'width', 'height')
    show_change_link = True  # Medyaya tıklandığında detay sayfasına yönlendirmek için

class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    show_change_link = True  # Mesaja tıklandığında detay sayfasına yönlendirmek için
    readonly_fields = ('bot_chat', 'sender', 'message_type', 'timestamp', 'status', 'reply_to_message', 'forward_from_message')

@admin.register(Bot)
class BotAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'platform_type', 'is_active')
    list_filter = ('platform_type', 'is_active')
    search_fields = ('name', 'user__username')
    ordering = ('user', 'platform_type')
    inlines = [ChatInline]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('token',)
        return ()

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('bot', 'chat_id', 'username', 'first_name', 'last_name', 'chat_type', 'title', 'is_active', 'joined_at', 'last_interaction')
    list_filter = ('bot', 'chat_type', 'is_active')
    search_fields = ('chat_id', 'username', 'first_name', 'last_name', 'title')
    inlines = [MessageInline]
    readonly_fields = ('bot', 'chat_id', 'username', 'first_name', 'last_name', 'chat_type', 'title', 'is_active', 'joined_at', 'last_interaction')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('bot_chat', 'sender', 'message_type', 'timestamp', 'status')
    list_filter = ('bot_chat', 'sender', 'message_type', 'status')
    search_fields = ('text', 'bot_chat__chat_id', 'bot_chat__username')
    inlines = [MediaInline]
    readonly_fields = ('bot_chat', 'sender', 'message_type', 'timestamp', 'status', 'reply_to_message', 'forward_from_message')

@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('chat_message', 'media_type', 'file_size', 'duration', 'width', 'height')
    list_filter = ('media_type',)
    search_fields = ('chat_message__text', 'chat_message__bot_chat__chat_id', 'chat_message__bot_chat__username')
    readonly_fields = ('chat_message', 'media_type', 'file_size', 'duration', 'width', 'height')