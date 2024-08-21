from django.contrib import admin

from .models.post import SocialMediaPlatform, Post, PlatformSpecificSchedule, PostMedia, FetchedPost

class PlatformSpecificScheduleInline(admin.TabularInline): 
    model = PlatformSpecificSchedule
    extra = 0  

class PostMediaInline(admin.TabularInline):
    model = PostMedia
    extra = 0

@admin.register(SocialMediaPlatform)
class SocialMediaPlatformAdmin(admin.ModelAdmin):
    list_display = ('name',) 

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'created_at')
    list_filter = ('user', 'created_at')
    search_fields = ('content', 'hashtags')
    inlines = [PlatformSpecificScheduleInline, PostMediaInline] 

# ... (PlatformSpecificScheduleAdmin and PostMediaAdmin remain the same)


admin.site.register(FetchedPost)