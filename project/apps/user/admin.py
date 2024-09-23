from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.html import format_html

from .models.custom_user import CustomUser
from .models.user_profile import Profile


@admin.action(description="Ban selected users")
def make_ban(self, request, queryset):
    queryset.update(is_banned=True)


class CustomUserAdmin(BaseUserAdmin):
    model = CustomUser
    ordering = ('email', 'created')
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active', 'is_banned', 'is_verified')
    list_filter = ('is_staff', 'is_active', 'is_verified')
    readonly_fields = ('slug', 'otp')
    actions = (make_ban,)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'slug', 'otp')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_banned', 'is_verified', 'user_permissions', 'groups')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'is_verified', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )
    search_fields = ('email',)
    filter_horizontal = ('user_permissions', 'groups')

admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(Profile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'display_image', 'profession',
        'phone_number', 'display_user'
    )
    list_filter = ('created',)
    search_fields = (
        'profession', 'description',
        'user__first_name',
        'user__last_name'
    )
    ordering = ('-updated',)
    date_hierarchy = 'created'
    list_per_page = 20
    readonly_fields = ('user', 'instagram_username')

    def display_user(self, obj):
        url = reverse("admin:user_customuser_change", args=[obj.user.id if obj.user else None])
        link = '<a style="color: red;" href="%s">%s</a>' % (
            url, 
            obj.user
        )
        return mark_safe(link)
    display_user.short_description = 'İstifadəçi'

    def display_image(self, obj):
        image = obj.image.url if obj.image else None
        raw_html = f'<img style="width:150px;height:auto;" src="{image}">'
        return format_html(raw_html)
    display_image.short_description = "Foto"

    def has_add_permission(self, request, obj=None):
        return False 

    # def has_change_permission(self, request, obj=None):
    #     return False