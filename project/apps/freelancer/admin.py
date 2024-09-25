from django.contrib import admin

from .models import FreelancerCategory


@admin.register(FreelancerCategory)
class FreeLancerCategoryAdmin(admin.ModelAdmin):
    readonly_fields = ('slug', )
