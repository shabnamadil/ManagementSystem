from django.contrib.auth import get_user_model 
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext as _

from rest_framework import serializers

from utils.serializers.password_field import PasswordField
from ..tasks import send_registration_otp

User = get_user_model()


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'full_name',
            'email',
            'user_profile' 
        )


class RegisterSerializer(serializers.ModelSerializer):
    password = PasswordField(write_only=True,  validators=[validate_password])
    password_confirm = PasswordField(write_only=True)

    class Meta:
        model = User
        extra_kwargs = {"password": {"write_only": True}}
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'password',
            'password_confirm'
        )

    def validate(self, attrs):
        password = attrs.get('password', '')
        password_confirm = self.initial_data.get('password_confirm', '')

        if not password_confirm:
            raise serializers.ValidationError({
                'password_confirm': _('This field is required.'),
            })
        
        if password != password_confirm:
            raise serializers.ValidationError({
                'password_confirm': _("Passwords do not match."),
            })
        
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')  # Remove password_confirm from validated_data
        user = User(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.is_active = False
        user.save()
        send_registration_otp.delay(user.email)
        return user
