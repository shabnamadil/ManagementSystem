from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.crypto import get_random_string
from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model

User = get_user_model()

from rest_framework import serializers

from apps.workspace.models import (
    Workspace,
    WorkspaceCategory,
    WorkspaceMember,
    WorkspaceInvitation,
    WorkspaceProject,
    ProjectMember,
    ProjectMemberInvitation
)
from apps.user.api.serializers import UserListSerializer


class WorkspaceMemberListSerializer(serializers.ModelSerializer):
    user = UserListSerializer()

    class Meta:
        model = WorkspaceMember
        fields = (
            'id',
            'user',
            'role'
        )


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
    workspace_project_count = serializers.SerializerMethodField()
    members_count = serializers.SerializerMethodField()
    tasks_count = serializers.SerializerMethodField()
    workspace_members = WorkspaceMemberListSerializer(many=True)

    class Meta:
        model = Workspace
        fields = (
            'id',
            'title',
            'description',
            'category',
            'workspace_members',
            'status',
            'creator',
            'workspace_project_count',
            'members_count',
            'tasks_count',
            'created_date',
            'get_absolute_url'
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
        if obj.workspace_members:
            return obj.workspace_members.count()
        return 0
    
    def get_tasks_count(self, obj):
        workspace_tasks_count = 0
        if obj.workspace_projects:
            for project in obj.workspace_projects.all():
                if project:
                        workspace_tasks_count += project.project_tasks.count()
            return workspace_tasks_count
        return workspace_tasks_count


class WorkspacePostSerializer(WorkspaceListSerializer):
    creator = serializers.PrimaryKeyRelatedField(read_only=True)
    workspace_members = serializers.SerializerMethodField()

    def validate(self, attrs):
        request = self.context['request']
        if not self.instance:
            attrs['creator'] = request.user
        return super().validate(attrs)

    def create(self, validated_data):
        creator = validated_data.pop('creator')
        workspace = Workspace.objects.create(**validated_data, creator=creator)
        
        WorkspaceMember.objects.create(
            user=creator, 
            role=WorkspaceMember.ROLE_CHOICES[3][1],
            workspace=workspace
        )
        
        return workspace

    def get_workspace_members(self, obj):
        return WorkspaceMemberListSerializer(obj.workspace_members.all(), many=True).data


class WorkspaceMemberInvitationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)

    class Meta:
        model = Workspace
        fields = (
            'id',
            'email',
        )

    def validate(self, attrs):
        request = self.context['request']
        email = attrs.get('email')
        workspace = self.instance
        inviter = request.user

        if not email:
            raise serializers.ValidationError("Email is required.")

        if self.instance.workspace_members.all():
            for member in self.instance.workspace_members.all():
                if member and member.user.email == email:
                    raise serializers.ValidationError("This user is already a member of the workspace.")

        # Generate the unique token
        token = get_random_string(length=32)
        uid = urlsafe_base64_encode(force_bytes(workspace.id))
        encoded_email = urlsafe_base64_encode(force_bytes(email))

        # Create the invitation link
        current_site = Site.objects.get_current()
        accept_url = f"http://{current_site.domain}{reverse_lazy('workspace-accept-invite', kwargs={'uid': uid, 'token': token, 'email': encoded_email})}"
        login_url = f"http://{current_site.domain}{reverse_lazy('login')}"

        # Prepare the email content
        context = {
            'workspace': workspace,
            'inviter': inviter,
            'accept_url': accept_url,
            'is_login' : User.objects.filter(email=email).exists(),
            'login_url': login_url
        }
        subject = f"{inviter} sizi '{workspace.title}' virtual ofisinə qoşulmağa dəvət edir."
        message = render_to_string('components/mail/workspace_invite.html', context)

        # Send the email
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
            html_message=message,
        )

        # Save the token in the database
        WorkspaceInvitation.objects.create(workspace=workspace, email=email, token=token)

        return attrs
    

class WorkspaceMemberRemoveSerializer(serializers.ModelSerializer):
    member = serializers.IntegerField()

    class Meta:
        model = Workspace
        fields = (
            'id',
            'workspace_members',
            'member'
            
        )

    def validate(self, attrs):
        member_id = attrs.get('member')
        workspace = self.instance
        
        try:
            member = workspace.workspace_members.get(id=member_id)
        except WorkspaceMember.DoesNotExist:
            raise serializers.ValidationError("This user is not a member of the workspace.")

        member.delete()
        
        return attrs


class WorkspaceMemberRoleUpdateSerializer(serializers.ModelSerializer):
    ROLE_CHOICES = [
        ('Adi üzv', 'Adi üzv'),
        ('Moderator', 'Moderator'),
        ('Admin', 'Admin'),
        ('Super admin', 'Super admin')
    ]
    member = serializers.IntegerField()
    role = serializers.ChoiceField(choices=ROLE_CHOICES)

    class Meta:
        model = Workspace
        fields = (
            'id',
            'workspace_members',
            'member',
            'role'
            
        )

    def validate(self, attrs):
        member_id = attrs.get('member')
        role = attrs.get('role')
        workspace = self.instance
        
        try:
            member = workspace.workspace_members.get(id=member_id)
            member.role = role
            member.save()
        except WorkspaceMember.DoesNotExist:
            raise serializers.ValidationError("This user is not a member of the workspace.")
        
        return attrs


class ProjectMemberListSerializer(serializers.ModelSerializer):
    user = UserListSerializer()

    class Meta:
        model = ProjectMember
        fields = (
            'id',
            'user',
            'role'
        )


class ProjectListSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField()
    tasks_count = serializers.SerializerMethodField()
    members_count = serializers.SerializerMethodField()
    project_members = ProjectMemberListSerializer(many=True)

    class Meta:
        model = WorkspaceProject
        fields = (
            'id',
            'title',
            'description',
            'workspace',
            'project_members',
            'creator',
            'tasks_count',
            'members_count',
            'created_date'
        )

    def get_creator(self, obj):
        if obj.creator.get_full_name():
            return obj.creator.get_full_name()
        return 'Admin User'
    
    def get_members_count(self, obj):
        if obj.project_members:
            return obj.project_members.count()
        return 0
    
    def get_tasks_count(self, obj):
        return obj.project_tasks.count()
    

class ProjectPostSerializer(ProjectListSerializer):
    creator = serializers.PrimaryKeyRelatedField(read_only=True)
    project_members = serializers.SerializerMethodField()

    def validate(self, attrs):
        request = self.context['request']
        if not self.instance:
            attrs['creator'] = request.user
        return super().validate(attrs)
    
    def get_project_members(self, obj):
        return ProjectMemberListSerializer(obj.project_members.all(), many=True).data
    
    def create(self, validated_data):
        creator = validated_data.pop('creator')
        project = WorkspaceProject.objects.create(**validated_data, creator=creator)
        
        ProjectMember.objects.create(
            user=creator, 
            role=ProjectMember.ROLE_CHOICES[1][1],
            project=project
        )
        
        return project
    

class ProjectMemberInvitationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)

    class Meta:
        model = WorkspaceProject
        fields = (
            'id',
            'email',
        )

    def validate(self, attrs):
        request = self.context['request']
        email = attrs.get('email')
        project = self.instance
        inviter = request.user

        if not email:
            raise serializers.ValidationError("Email is required.")

        if self.instance.project_members.all():
            for member in self.instance.project_members.all():
                if member and member.user.email == email:
                    raise serializers.ValidationError("This user is already a member of the workspace.")

        # Generate the unique token
        token = get_random_string(length=32)
        uid = urlsafe_base64_encode(force_bytes(project.id))
        encoded_email = urlsafe_base64_encode(force_bytes(email))

        # Create the invitation link
        current_site = Site.objects.get_current()
        accept_url = f"http://{ current_site.domain }{reverse_lazy('project-accept-invite', kwargs={'uid': uid, 'token': token, 'email': encoded_email})}"
        login_url = f"http://{ current_site.domain }{reverse_lazy('login')}"

        # Prepare the email content
        context = {
            'project': project,
            'inviter': inviter,
            'accept_url': accept_url,
            'is_login' : User.objects.filter(email=email).exists(),
            'login_url': login_url
        }
        subject = f"{inviter} sizi '{project.title}' layihəsinə qoşulmağa dəvət edir."
        message = render_to_string('components/mail/project_invite.html', context)

        # Send the email
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
            html_message=message,
        )

        # Save the token in the database
        ProjectMemberInvitation.objects.create(project=project, email=email, token=token)

        return attrs
    

class ProjectMemberRemoveSerializer(serializers.ModelSerializer):
    member = serializers.IntegerField()

    class Meta:
        model = WorkspaceProject
        fields = (
            'id',
            'project_members',
            'member'
            
        )

    def validate(self, attrs):
        member_id = attrs.get('member')
        project = self.instance
        
        try:
            member = project.project_members.get(id=member_id)
        except ProjectMember.DoesNotExist:
            raise serializers.ValidationError("This user is not a member of the workspace.")

        member.delete()
        
        return attrs


class ProjectMemberRoleUpdateSerializer(serializers.ModelSerializer):
    ROLE_CHOICES = [
        ('Adi üzv', 'Adi üzv'),
        ('Moderator', 'Moderator'),
        ('Admin', 'Admin'),
    ]
    member = serializers.IntegerField()
    role = serializers.ChoiceField(choices=ROLE_CHOICES)

    class Meta:
        model = WorkspaceProject
        fields = (
            'id',
            'project_members',
            'member',
            'role'
            
        )

    def validate(self, attrs):
        member_id = attrs.get('member')
        role = attrs.get('role')
        project = self.instance
        
        try:
            member = project.project_members.get(id=member_id)
            member.role = role
            member.save()
        except ProjectMember.DoesNotExist:
            raise serializers.ValidationError("This user is not a member of the workspace.")
        
        return attrs