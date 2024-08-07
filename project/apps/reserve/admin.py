from django.contrib import admin

from .models.bot_config import BotConfig

    
@admin.register(BotConfig)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'token')

    