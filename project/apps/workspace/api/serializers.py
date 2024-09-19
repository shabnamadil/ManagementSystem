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
from django.utils import timezone

User = get_user_model()

from rest_framework import serializers

from apps.workspace.models import (
    Workspace,
    WorkspaceCategory,
    WorkspaceMember,
    WorkspaceInvitation,
    WorkspaceProject,
    ProjectMember,
    ProjectMemberInvitation,
    Task,
    TaskAssignedMember,
    TaskInvitation,
    Subtask,
    SubtaskStatus,
    TaskSentTo
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
            'get_absolute_url',
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
    

class TaskAssignedMemberListSerializer(serializers.ModelSerializer):
    user = UserListSerializer()

    class Meta:
        model = TaskAssignedMember
        fields = (
            'id',
            'user',
            'role'
        )


class TaskListSerializer(serializers.ModelSerializer):
    task_creator = serializers.SerializerMethodField()
    assigned_members  = TaskAssignedMemberListSerializer(many=True)
    started = serializers.SerializerMethodField()
    deadline = serializers.SerializerMethodField()
    members_count = serializers.SerializerMethodField()
    subtasks_count = serializers.SerializerMethodField()
    sharing_date=serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = (
            'id',
            'title',
            'description',
            'content',
            'assigned_members',
            'file',
            'ready_content',
            'priority',
            'task_creator',
            'project',
            'completed_percent',
            'completed',
            'members_count',
            'subtasks_count',
            'get_absolute_url',
            'started',
            'deadline',
            'created_date',
            'sharing_date',
            'client_accepted'
        )

    def get_task_creator(self, obj):
        if obj.task_creator.get_full_name():
            return obj.task_creator.get_full_name()
        return 'Admin User'
    
    def get_deadline(self, obj):
        local = timezone.localtime(obj.deadline)
        return local.strftime('%d/%m/%Y, %H:%M')
    
    def get_started(self, obj):
        local = timezone.localtime(obj.started)
        return local.strftime('%d/%m/%Y, %H:%M')
    
    def get_sharing_date(self, obj):
        if obj.sharing_date:
            local = timezone.localtime(obj.sharing_date)
            return local.strftime('%d/%m/%Y, %H:%M')
    
    def get_members_count(self, obj):
        if obj.assigned_members:
            return obj.assigned_members.count()
        return 0
    
    def get_subtasks_count(self, obj):
        if obj.subtasks:
            return obj.subtasks.count()
        return 0
    

class TaskPostSerializer(TaskListSerializer):
    PRIORITY_CHOICES = [
        ('Highest', 'Highest'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
        ('Lowest', 'Lowest')
    ]
        
    task_creator = serializers.PrimaryKeyRelatedField(read_only=True)
    assigned_members = serializers.SerializerMethodField()
    priority = serializers.ChoiceField(choices=PRIORITY_CHOICES)
    started = serializers.DateTimeField()
    deadline = serializers.DateTimeField()
    sharing_date = serializers.DateTimeField(required=False, allow_null=True)

    def validate(self, attrs):
        request = self.context['request']
        if not self.instance:
            attrs['task_creator'] = request.user
        started = attrs.get('started', None)
        deadline = attrs.get('deadline', None)

        if self.instance:
            # If instance exists, use the original dates if not updated
            if started is None:
                started = self.instance.started
            if deadline is None:
                deadline = self.instance.deadline

        # Validate deadline is after start date
        if started and deadline and deadline <= started:
            raise ValidationError('Deadline must be in the future')

        # Validate that the start date is not in the past, but only if it's being changed
        if self.instance is None or (started and started != self.instance.started):
            if started < timezone.now():
                raise ValidationError('Start date cannot be in the past')

        return attrs
    
    def create(self, validated_data):
        task_creator = validated_data.pop('task_creator')
        task = Task.objects.create(**validated_data, task_creator=task_creator)
        
        TaskAssignedMember.objects.create(
            user=task_creator, 
            role=TaskAssignedMember.ROLE_CHOICES[2][1],
            task=task
        )
        
        return task
    
    def update(self, instance, validated_data):
        # Handle file: retain existing file if no new file is uploaded
        if not validated_data.get('file') and instance.file:
            validated_data['file'] = instance.file

        return super().update(instance, validated_data)

    def get_assigned_members(self, obj):
        return TaskAssignedMemberListSerializer(obj.assigned_members.all(), many=True).data
    

class TaskMemberInvitationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)

    class Meta:
        model = Task
        fields = (
            'id',
            'email',
        )

    def validate(self, attrs):
        request = self.context['request']
        email = attrs.get('email')
        task = self.instance
        inviter = request.user

        if not email:
            raise serializers.ValidationError("Email is required.")

        if self.instance.assigned_members.all():
            for member in self.instance.assigned_members.all():
                if member and member.user.email == email:
                    raise serializers.ValidationError("This user is already a member of the task.")

        # Generate the unique token
        token = get_random_string(length=32)
        uid = urlsafe_base64_encode(force_bytes(task.id))
        encoded_email = urlsafe_base64_encode(force_bytes(email))

        # Create the invitation link
        current_site = Site.objects.get_current()
        accept_url = f"http://{current_site.domain}{reverse_lazy('task-accept-invite', kwargs={'uid': uid, 'token': token, 'email': encoded_email})}"
        login_url = f"http://{current_site.domain}{reverse_lazy('login')}"

        # Prepare the email content
        context = {
            'task': task,
            'inviter': inviter,
            'accept_url': accept_url,
            'is_login' : User.objects.filter(email=email).exists(),
            'login_url': login_url
        }
        subject = f"{inviter} sizi '{task.title}' taskina qoşulmağa dəvət edir."
        message = render_to_string('components/mail/task_invite.html', context)

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
        TaskInvitation.objects.create(task=task, email=email, token=token)

        return attrs
   

class TaskCompletedSerializer(TaskListSerializer):

    def update(self, instance, validated_data):
        if instance.subtasks.count() == 0:
            if instance.completed:
                validated_data['completed'] = False
            else:
                validated_data['completed'] = True
        else:
            if all(subtask.completed for subtask in instance.subtasks.all()):
                validated_data['completed'] = True
            else:
                validated_data['completed'] = False

        return super().update(instance, validated_data)
    

class TaskAddMemberSerializer(serializers.ModelSerializer):
    member_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Task
        fields = (
            'id',
            'member_id'
        )

    def create(self, validated_data):
        member_id = validated_data.pop('member_id')
        return member_id
    
    def update(self, instance, validated_data):
        # Handle file: retain existing file if no new file is uploaded
        user = User.objects.get(id=validated_data.get('member_id'))
        TaskAssignedMember.objects.create(
            user = user,
            role='Adi üzv',
            task=instance
        )

        return super().update(instance, validated_data)
    
    def validate(self, attrs):
        user = User.objects.get(id=attrs['member_id'])

        if TaskAssignedMember.objects.get(user=user):
            raise ValidationError('This user is already member of this task')
        
        return super().validate(attrs)
    

class TaskSendToSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)

    class Meta:
        model = TaskSentTo
        fields = (
            'id',
            'email',
            'task'
        )

    def validate(self, attrs):
        request = self.context['request']
        email = attrs.get('email')
        task = attrs.get('task')
        inviter = request.user

        if not email:
            raise serializers.ValidationError("Email is required.")
        if not task.completed:
            raise serializers.ValidationError('Task must be completed before sharing.')
        

        try:
            user = User.objects.get(email=email)
            try:
                sended_to = TaskSentTo.objects.get(task=task, user=user)
                if sended_to:
                    raise serializers.ValidationError('Task is already sent to this email')
            except TaskSentTo.DoesNotExist:
                sended_to = None
        except User.DoesNotExist:
            user = None

        # Prepare the email content
        current_site = Site.objects.get_current()
        send_url = f"http://{current_site.domain}/{task.get_absolute_url()}"
        login_url = f"http://{current_site.domain}{reverse_lazy('login')}"

        context = {
            'task': task,
            'inviter': inviter,
            'send_url': send_url,
            'is_login': user is not None,
            'login_url': login_url
        }
        subject = "Taska nəzər"
        message = render_to_string('components/mail/task_send_to.html', context)

        # Send the email
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
            html_message=message,
        )

        self.context['user'] = user

        return attrs

    def create(self, validated_data):
        validated_data.pop('email', None)
        user = self.context.get('user')

        if user:
            validated_data['user'] = user

        return TaskSentTo.objects.create(**validated_data)
    

class TaskClientEditSerializer(serializers.ModelSerializer):
    file = serializers.FileField(read_only=True)
    title = serializers.CharField(read_only=True)

    class Meta:
        model = Task
        fields = (
            'id',
            'ready_content',
            'task_sent_to',
            'file',
            'title'
        )

    def validate(self, attrs):
        if not attrs.get('task_sent_to'):
            raise serializers.ValidationError('This task has to be sent to someone before this action.')
        return super().validate(attrs)
    

class TaskClientAcceptSerializer(serializers.ModelSerializer):
    title = serializers.CharField(read_only=True)
    completed_percent = serializers.IntegerField(read_only=True)

    class Meta:
        model = Task
        fields = (
            'id',
            'client_accepted',
            'title',
            'completed_percent'
        )

    def update(self, instance, validated_data):
        validated_data['client_accepted'] = not instance.client_accepted
        instance = super().update(instance, validated_data)
        instance.save()
        return instance
    

class SubtaskListSerializer(serializers.ModelSerializer):
    subtask_creator = serializers.SerializerMethodField()
    started_date = serializers.SerializerMethodField()
    deadline = serializers.SerializerMethodField()
    assigned_user = serializers.SerializerMethodField()
    subtask_task_admin = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = Subtask
        fields = (
            'id', 
            'job',
            'subtask_creator',
            'task',
            'started_date',
            'deadline',
            'content',
            'file',
            'completed',
            'assigned_to',
            'assigned_user',
            'subtask_task_admin',
            'status'
        )

    def get_subtask_creator(self, obj):
        if obj.subtask_creator.get_full_name():
            return obj.subtask_creator.get_full_name()
        return 'Admin User'
    
    def get_deadline(self, obj):
        local = timezone.localtime(obj.deadline)
        return local.strftime('%d/%m/%Y, %H:%M')
    
    def get_started_date(self, obj):
        local = timezone.localtime(obj.started_date)
        return local.strftime('%d/%m/%Y, %H:%M')
    
    def get_assigned_user(self, obj):
        if obj.assigned_to:
            return TaskAssignedMemberListSerializer(obj.assigned_to).data
        
    def get_subtask_task_admin(self, obj):
        admins = obj.task.assigned_members.filter(role='Admin')
        return TaskAssignedMemberListSerializer(admins, many=True).data
    
    def get_status(self, obj):
        data = {
            'status_name' : obj.status.status_name,
            'status_id' : obj.status.id
        }
        return data


class SubtaskPostSerializer(SubtaskListSerializer):
    subtask_creator = serializers.PrimaryKeyRelatedField(read_only=True)
    completed = serializers.SerializerMethodField()
    started_date = serializers.DateTimeField()
    deadline = serializers.DateTimeField()
    assigned_to = TaskAssignedMemberListSerializer


    def validate(self, attrs):
        request = self.context['request']
        if not self.instance:
            attrs['subtask_creator'] = request.user
        if attrs['started_date'] and attrs['deadline']:
            if attrs['deadline'] <= attrs['started_date']:
                raise ValidationError('Deadline must be in the future')
        if attrs['started_date']:
            if attrs['started_date'] < timezone.now():
                raise ValidationError('Started date cannot be in the past')
        if attrs['assigned_to']:
            if attrs['task'] != attrs['assigned_to'].task:
                raise ValidationError('Subtask can only be assigned to related task members')
        return super().validate(attrs)
    
    
    def get_completed(self, obj):
        return obj.completed
    

class SubtaskCompletedSerializer(SubtaskListSerializer):

    def update(self, instance, validated_data):
        validated_data['completed'] = not instance.completed
        instance = super().update(instance, validated_data)
        task = instance.task
        if all(subtask.completed for subtask in task.subtasks.all()):
            task.completed = True
        else:
            task.completed = False
        task.save()
        return instance
    

class SubtaskAddMemberSerializer(serializers.ModelSerializer):
    member_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Subtask
        fields = (
            'id',
            'member_id'
        )

    def create(self, validated_data):
        member_id = validated_data.pop('member_id')
        return member_id
    
    def update(self, instance, validated_data):
        # Handle file: retain existing file if no new file is uploaded
        user = User.objects.get(id=validated_data.get('member_id'))
        TaskAssignedMember.objects.create(
            user = user,
            role='Adi üzv',
            task=instance
        )

        return super().update(instance, validated_data)
    
    def validate(self, attrs):
        user = User.objects.get(id=attrs['member_id'])

        if TaskAssignedMember.objects.get(user=user):
            raise ValidationError('This user is already member of this task')
        
        return super().validate(attrs)
    

class SubtaskAcceptedSerializer(SubtaskListSerializer):

    def update(self, instance, validated_data):
        if instance.status.status_name == 'In progress':
            instance.status.status_name = 'Accepted'
            instance.status.save()
        return super().update(instance, validated_data)
    

class SubtaskAddNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubtaskStatus
        fields = (
            'id',
            'note'
        )

    def update(self, instance, validated_data):
        if instance.status_name == 'Accepted':
            instance.status_name = 'In progress'
            instance.save()
        if instance.subtask.completed == True:
            instance.subtask.completed = False
            instance.subtask.save()
        return super().update(instance, validated_data)


