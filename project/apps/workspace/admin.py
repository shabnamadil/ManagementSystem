from django.contrib import admin

from .models.workspace import (
    Workspace, 
    WorkspaceCategory, 
    WorkspaceUser
)

#Workspace.py
admin.site.register(WorkspaceCategory)

class WorkspaceUserInline(admin.TabularInline):
    model = WorkspaceUser
    autocomplete_fields = ['user',]  # Kullanıcı için autocomplete özelliği
    # readonly_fields = ['is_creator']

@admin.register(Workspace)
class WorkspaceAdmin(admin.ModelAdmin):
    inlines = [WorkspaceUserInline, ]
    readonly_fields = ["slug", ]