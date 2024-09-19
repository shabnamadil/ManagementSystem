from django.contrib.auth import get_user_model 
from django.contrib.auth.password_validation import validate_password
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.contrib.sites.models import Site

from rest_framework import serializers

from utils.serializers.password_field import PasswordField
from ..tokens import account_activation_token

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
        password = attrs['password']
        if 'password_confirm' in self.initial_data and password != self.initial_data['password_confirm']:
            raise serializers.ValidationError("Passwords do not match")
        if 'password_confirm' not in self.initial_data:
            raise serializers.ValidationError('it is missed password_confirm')
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
        current_site = Site.objects.get_current()
        subject = 'Activate TaskFries Account'
        message = render_to_string('components/mail/account_activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        user.email_user(subject, message)
        return user
