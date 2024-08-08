from rest_framework import serializers

from apps.workspace.models import Workspace
from apps.user.api.serializers import UserListSerializer


class WorkspaceListSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField()
    members = UserListSerializer(many=True)
    admins = UserListSerializer(many=True)

    class Meta:
        model = Workspace
        fields = (
            'id',
            'title',
            'description',
            'members',
            'admins',
            'super_admin',
            'status',
            'creator'
        )

    def get_creator(self, obj):
        if obj.creator.get_full_name():
            return obj.creator.get_full_name()
        return 'Admin User'
    

class WorkspacePostSerializer(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Workspace
        fields = (
            'id',
            'title',
            'description',
            'members',
            'admins',
            'super_admin',
            'status',
            'creator'
        )

    def validate(self, attrs):
        request = self.context['request']
        if not self.instance:
            attrs['creator'] = request.user
        return super().validate(attrs)