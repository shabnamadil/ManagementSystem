from django.contrib import admin

from .models import Contact
from .forms import ContactForm


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'email', 'mobile_number')
    list_filter = ('created', )
    date_hierarchy = 'created'
    list_per_page = 20
    search_fields = ('name', 'surname', 'email', 'message')
    form = ContactForm

    def get_full_name(self, obj):
        return f'{obj.name} {obj.surname}'
    get_full_name.short_description = 'Ad, Soyad'