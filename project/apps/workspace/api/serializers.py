from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from rest_framework import serializers

from apps.workspace.models import (
    Workspace,
    WorkspaceCategory
)
from apps.user.api.serializers import UserListSerializer


class WorkspaceCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkspaceCategory
        fields = (
            'id',
            'name',
            'color',
            'file'
        )


class WorkspaceListSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField()
    members = UserListSerializer(many=True)
    admins = UserListSerializer(many=True)
    workspace_project_count = serializers.SerializerMethodField()
    members_count = serializers.SerializerMethodField()
    tasks_count = serializers.SerializerMethodField()
    status_color = serializers.SerializerMethodField()

    class Meta:
        model = Workspace
        fields = (
            'id',
            'title',
            'description',
            'category',
            'members',
            'admins',
            'super_admin',
            'status',
            'creator',
            'workspace_project_count',
            'members_count',
            'tasks_count',
            'created_date',
            'status_color',
            'slug'
        )

    def get_creator(self, obj):
        if obj.creator.get_full_name():
            return obj.creator.get_full_name()
        return 'Admin User'
    
    def get_workspace_project_count(self, obj):
        if obj.workspace_projects:
            return obj.workspace_projects.count()
        return 0
    
    def get_members_count(self, obj):
        if obj.members:
            return obj.members.count()
        return 0
    
    def get_tasks_count(self, obj):
        workspace_tasks_count = 0
        if obj.workspace_projects:
            for workspace_project in obj.workspace_projects.all():
                if workspace_project:
                    for client_project in workspace_project.client_projects.all():
                        if client_project:
                            workspace_tasks_count += client_project.project_tasks.count()
            return workspace_tasks_count
        return workspace_tasks_count
    
    def get_status_color(self, obj):
        if obj.status == 'public':
            return 'light-orange-bg'
        return 'light-success-bg'


class WorkspacePostSerializer(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(read_only=True)
    super_admin = serializers.PrimaryKeyRelatedField(read_only=True)
    workspace_project_count = serializers.SerializerMethodField()
    members_count = serializers.SerializerMethodField()
    tasks_count = serializers.SerializerMethodField()
    status_color = serializers.SerializerMethodField()

    class Meta:
        model = Workspace
        fields = (
            'id',
            'title',
            'description',
            'category',
            'members',
            'admins',
            'super_admin',
            'status',
            'creator',
            'workspace_project_count',
            'members_count',
            'tasks_count',
            'created_date',
            'status_color',
        )

    def validate(self, attrs):
        request = self.context['request']
        if not self.instance:
            attrs['creator'] = request.user
            attrs['admins'].append(request.user)
            attrs['members'].append(request.user)
            attrs['super_admin'] = request.user
        return super().validate(attrs)
    
    def get_workspace_project_count(self, obj):
        if obj.workspace_projects:
            return obj.workspace_projects.count()
        return 0
    
    def get_members_count(self, obj):
        if obj.members:
            return obj.members.count()
        return 0
    
    def get_tasks_count(self, obj):
        workspace_tasks_count = 0
        if obj.workspace_projects:
            for workspace_project in obj.workspace_projects.all():
                if workspace_project:
                    for client_project in workspace_project.client_projects.all():
                        if client_project:
                            workspace_tasks_count += client_project.project_tasks.count()
            return workspace_tasks_count
        return workspace_tasks_count
    
    def get_status_color(self, obj):
        if obj.status == 'public':
            return 'light-orange-bg'
        return 'light-success-bg'
    

class WorkspaceMemberInvitationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Workspace
        fields = (
            'id',
            'members',
        )

    def validate(self, attrs):
        request = self.context['request']
        email = request.data.get('email')
        return super().validate(attrs)