from django.contrib import admin

from .models import AboutUs, Team


class SingletonModelAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        """Prevent adding more than one instance."""
        return not self.model.objects.exists()

    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of the singleton instance."""
        return False


@admin.register(AboutUs)
class AboutUsAdmin(SingletonModelAdmin):
    pass


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'profession')