from typing import Any
from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import (
    Workspace,
    WorkspaceCategory,
    WorkspaceMember,
    WorkspaceInvitation,
    WorkspaceProject,
    ProjectMember,
    ProjectMemberInvitation,
    Task,
    Subtask,
    TaskAssignedMember,
    SubtaskStatus,
    TaskSentTo
)

admin.site.register(Subtask)
admin.site.register(TaskAssignedMember)
admin.site.register(SubtaskStatus)
admin.site.register(TaskSentTo)

@admin.action(description="Make banned selected workspaces")
def make_ban(self, request, queryset):
    queryset.update(is_banned=True)
    

@admin.register(Workspace)
class WorkspaceAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'display_description',
        'display_creator', 'category',
        'display_created_date',
        'is_banned',
    )
    list_filter = ('created', 'category', 'is_banned')
    search_fields = (
        'title', 'description', 'category__name'
    )
    ordering = ('-updated', 'title')
    date_hierarchy = 'created'
    list_per_page = 20
    # readonly_fields = (
    #     'title', 'description', 
    #     'members', 'admins',
    #     'creator', 'slug', 
    #     'super_admin', 'status',
    #     'category'
    # )
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

    # def has_add_permission(self, request, obj=None):
    #     return False 


@admin.register(WorkspaceProject)
class WorkspaceProjectAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'display_description',
        'display_creator', 'display_workspace',
        'display_created_date'
    )
    list_filter = ('created',)
    search_fields = (
        'title', 'description', 'workspace__title'
    )
    ordering = ('-updated', 'title')
    date_hierarchy = 'created'
    list_per_page = 20
    # readonly_fields = (
    #     'title', 'description', 
    #     'creator', 'slug', 'workspace'
    # )

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
    display_creator.short_description = 'Layihəni yaratdı'

    def display_workspace(self, obj):
        url = reverse("admin:workspace_workspace_change", args=[obj.workspace.id])
        link = '<a style="color: red;" href="%s">%s</a>' % (
            url, 
            obj.workspace
        )
        return mark_safe(link)
    display_workspace.short_description = 'Virtual ofis'

    def display_created_date(self, obj):
        return obj.created_date
    display_created_date.short_description = 'Yaranma tarixi'

    # def has_add_permission(self, request, obj=None):
    #     return False

    # def has_delete_permission(self, request, obj=None):
    #     return False 

    # def has_change_permission(self, request, obj=None):
    #     return False


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'display_content',
        'project', 'display_assigned_to',
        'completed_percent', 'display_deadline'
    )
    list_filter = ('created', 'deadline')
    search_fields = (
        'title', 'content',
    )
    ordering = ('-updated', 'title')
    date_hierarchy = 'created'
    list_per_page = 20
    # readonly_fields = (
    #     'title', 'content',
    #     'project', 'file',
    #     'task_assigned_to',
    #     'deadline',
    #     'task_creator', 'slug'
    # )

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.task_creator = request.user
        super().save_model(request, obj, form, change)

    def display_content(self, obj):
        return obj.truncated_content
    display_content.short_description = 'Qısa təsvir'

    def display_assigned_to(self, obj):
        assigned_users = [user.user.email for user in obj.assigned_members.all()]
        return assigned_users
    display_assigned_to.short_description = 'Taskı yerinə yetirməlidir'

    def display_deadline(self, obj):
        return obj.deadline.strftime('%d/%m/%Y, %H:%M')
    display_deadline.short_description = 'Taskın bitmə tarixi'

    # def has_add_permission(self, request, obj=None):
    #     return False 

    # def has_delete_permission(self, request, obj=None):
    #     return False 

    # def has_change_permission(self, request, obj=None):
    #     return False
    

@admin.register(WorkspaceCategory)
class WorkspaceCategoryAdmin(admin.ModelAdmin):
    readonly_fields = ('slug',)


@admin.register(WorkspaceMember)
class WorkspaceMemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'workspace', 'created_date')
    list_filter = ('role', 'user', 'workspace')
    readonly_fields = ('user', 'role', 'workspace')
    search_fields = ('user__email', 'role', 'workspace__title')
    ordering = ('role', )
    list_per_page = 20
    date_hierarchy = 'created'

    # def has_add_permission(self, request, obj=None):
    #     return False 

    # def has_delete_permission(self, request, obj=None):
    #     return False 

    # def has_change_permission(self, request, obj=None):
    #     return False


@admin.register(ProjectMember)
class ProjetctMemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'project', 'created_date')
    list_filter = ('role', 'user', 'project')
    readonly_fields = ('user', 'role', 'project')
    search_fields = ('user__email', 'role', 'project__title')
    ordering = ('role', )
    list_per_page = 20
    date_hierarchy = 'created'

    # def has_add_permission(self, request, obj=None):
    #     return False 

    # def has_delete_permission(self, request, obj=None):
    #     return False 

    # def has_change_permission(self, request, obj=None):
    #     return False


@admin.register(WorkspaceInvitation)
class WorkspaceinvitationAdmin(admin.ModelAdmin):
    list_display = ('email', 'workspace', 'is_accepted', 'created_date')
    list_filter = ('is_accepted', 'workspace')
    search_fields = ('email', 'workspace__title')
    readonly_fields = ('email', 'workspace', 'is_accepted', 'token')
    ordering = ('-created',)
    list_per_page = 20
    date_hierarchy = 'created'

    # def has_add_permission(self, request, obj=None):
    #     return False 

    # def has_delete_permission(self, request, obj=None):
    #     return False 

    # def has_change_permission(self, request, obj=None):
    #     return False


@admin.register(ProjectMemberInvitation)
class ProjectMemberInvitationAdmin(admin.ModelAdmin):
    list_display = ('email', 'project', 'is_accepted', 'created_date')
    list_filter = ('is_accepted', 'project')
    search_fields = ('email', 'project__title')
    readonly_fields = ('email', 'project', 'is_accepted', 'token')
    ordering = ('-created',)
    list_per_page = 20
    date_hierarchy = 'created'

    # def has_add_permission(self, request, obj=None):
    #     return False 

    # def has_delete_permission(self, request, obj=None):
    #     return False 

    # def has_change_permission(self, request, obj=None):
    #     return False