from typing import Any
from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import (
    Workspace,
    WorkspaceClientProject,
    WorkspaceProject,
    Task
)

from .forms import (
    WorkspaceForm,
    WorkspaceProjectForm,
    WorkspaceClientProjectForm,
    TaskForm
)


@admin.action(description="Make banned selected workspaces")
def make_ban(self, request, queryset):
    queryset.update(is_banned=True)


class WorkspaceProjectInline(admin.TabularInline):
    model = WorkspaceProject
    readonly_fields = ('client', 'moderator')
    classes = ('collapse',)
    form = WorkspaceProjectForm
    extra = 0

    def has_add_permission(self, request, obj):
        return False 

    def has_delete_permission(self, request, obj):
        return False 

    def has_change_permission(self, request, obj):
        return False
    

@admin.register(Workspace)
class WorkspaceAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'display_description',
        'display_creator',
        'display_created_date',
        'is_banned',
    )
    list_filter = ('created', 'is_banned')
    search_fields = (
        'title', 'description',
    )
    ordering = ('-updated', 'title')
    date_hierarchy = 'created'
    list_per_page = 20
    readonly_fields = (
        'title', 'description', 
        'members', 'admins',
        'creator', 'slug', 
        'super_admin', 'status'
    )
    inlines = (WorkspaceProjectInline, )
    form = WorkspaceForm
    actions = (make_ban,)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.creator = request.user
        super().save_model(request, obj, form, change)

    def display_description(self, obj):
        return obj.truncated_description
    display_description.short_description = 'Qısa təsvir'

    def display_creator(self, obj):
        url = reverse("admin:user_customuser_change", args=[obj.creator.id])
        link = '<a style="color: red;" href="%s">%s</a>' % (
            url, 
            obj.creator.email
        )
        return mark_safe(link)
    display_creator.short_description = 'Virtual ofis yaratdı'

    def display_created_date(self, obj):
        return obj.created_date
    display_created_date.short_description = 'Yaranma tarixi'

    def has_add_permission(self, request, obj=None):
        return False 


@admin.register(WorkspaceClientProject)
class WorkspaceClientProjectAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'display_description',
        'workspace_project',
        'display_moderator',
        'display_created_date'
    )
    list_filter = ('created',)
    search_fields = (
        'title', 'description',
    )
    ordering = ('-updated', 'title')
    date_hierarchy = 'created'
    list_per_page = 20
    readonly_fields = (
        'title', 'description',
        'workspace_project', 'moderator',
        'slug'
    )
    form = WorkspaceClientProjectForm

    def display_description(self, obj):
        return obj.truncated_description
    display_description.short_description = 'Qısa təsvir'

    def display_moderator(self, obj):
        url = reverse("admin:user_customuser_change", args=[obj.moderator.id if obj.moderator else None])
        link = '<a style="color: red;" href="%s">%s</a>' % (
            url, 
            obj.moderator
        )
        return mark_safe(link)
    display_moderator.short_description = 'Müştəri layihə rəhbəri'

    def display_created_date(self, obj):
        return obj.created_date
    display_created_date.short_description = 'Yaranma tarixi'

    def has_add_permission(self, request, obj=None):
        return False 

    def has_delete_permission(self, request, obj=None):
        return False 

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'display_content',
        'project', 'display_assigned_to',
        'display_deadline'
    )
    list_filter = ('created', 'deadline')
    search_fields = (
        'title', 'content',
    )
    ordering = ('-updated', 'title')
    date_hierarchy = 'created'
    list_per_page = 20
    readonly_fields = (
        'title', 'content',
        'project', 'file',
        'task_assigned_to',
        'deadline',
        'task_creator', 'slug'
    )
    form = TaskForm

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.task_creator = request.user
        super().save_model(request, obj, form, change)

    def display_content(self, obj):
        return obj.truncated_content
    display_content.short_description = 'Qısa təsvir'

    def display_assigned_to(self, obj):
        assigned_users = [user.email for user in obj.task_assigned_to.all()]
        return assigned_users
    display_assigned_to.short_description = 'Taskı yerinə yetirməlidir'

    def display_deadline(self, obj):
        return obj.deadline.strftime('%d/%m/%Y, %H:%M')
    display_deadline.short_description = 'Taskın bitmə tarixi'

    def has_add_permission(self, request, obj=None):
        return False 

    def has_delete_permission(self, request, obj=None):
        return False 

    def has_change_permission(self, request, obj=None):
        return False