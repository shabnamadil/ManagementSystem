from django.contrib import admin

from .models import SiteSettings
from .forms import SiteSettingsForm


class SingletonModelAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        """Prevent adding more than one instance."""
        return not self.model.objects.exists()

    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of the singleton instance."""
        return False


@admin.register(SiteSettings)
class SiteSettingsAdmin(SingletonModelAdmin):
    list_display = ('site_name',)
    form = SiteSettingsForm