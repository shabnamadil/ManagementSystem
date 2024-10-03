from django.contrib.auth import get_user_model 
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError

from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from utils.serializers.password_field import PasswordField
from ..tasks import send_registration_otp
from ..models import Profile

User = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Profile
        fields = (
            'id',
            'image',
            'profession',
            'description',
            'phone_number',
            'facebook_link',
            'instagram_link',
            'tiktok_link',
            'youtube_link'
        )


class UserListSerializer(serializers.ModelSerializer):
    user_profile = UserProfileSerializer()

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
    

class UserUpdateDestroySerializer(serializers.ModelSerializer):
    user_profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'user_profile'
        )

    def update(self, instance, validated_data):
        # Extract the nested user_profile data
        user_profile_data = validated_data.pop('user_profile', None)
        
        # Update the user instance fields
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        # Update the user_profile instance fields
        if user_profile_data:
            user_profile = instance.user_profile

            # Only update the image if it's provided in the request
            if 'image' in user_profile_data:
                if user_profile_data['image'] is not None:
                    user_profile.image = user_profile_data['image']
                else:
                    # If 'image' is explicitly None, keep the current image or handle as needed
                    pass

            user_profile.profession = user_profile_data.get('profession', user_profile.profession)
            user_profile.description = user_profile_data.get('description', user_profile.description)
            user_profile.phone_number = user_profile_data.get('phone_number', user_profile.phone_number)
            user_profile.facebook_link = user_profile_data.get('facebook_link', user_profile.facebook_link)
            user_profile.instagram_link = user_profile_data.get('instagram_link', user_profile.instagram_link)
            user_profile.tiktok_link = user_profile_data.get('phone_number', user_profile.tiktok_link)
            user_profile.youtube_link = user_profile_data.get('phone_number', user_profile.youtube_link)
            
            user_profile.save()

        return instance
    
    def validate(self, attrs):
        user_profile_data = attrs.get('user_profile')

        if user_profile_data:
            phone_number = user_profile_data.get('phone_number', '')

            if phone_number and phone_number.startswith('+'):
                phone_number_without_plus = phone_number[1:]
            else:
                phone_number_without_plus = phone_number

            if phone_number_without_plus and not phone_number_without_plus.isdigit():
                raise ValidationError({'phone_number': 'Only numeric values are allowed.'})
            if phone_number_without_plus and len(phone_number_without_plus) < 10:
                raise ValidationError({'phone_number': 'Mobile number must be at least 10 characters.'})
            if user_profile_data['profession'] and len(user_profile_data['profession']) < 5:
                raise ValidationError('Profession must be at least 5 characters')
            
        return super().validate(attrs)
    

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # Get the refresh token object
        refresh = self.get_token(self.user)

        # Get the access token from the refresh token
        access_token = refresh.access_token

        # Add the refresh token jti to the access token payload
        access_token['refresh_jti'] = str(refresh['jti']) 

        # Return the tokens as strings, not as objects
        data['access'] = str(access_token)
        data['refresh'] = str(refresh)

        # Add user-related data to the response
        data.update({
            'user': {
                'id': self.user.id,
                'full_name': self.user.full_name,
                'email': self.user.email,
                'profile': {
                    'profession': self.user.user_profile.profession,
                    'description': self.user.user_profile.description,
                    'phone_number': self.user.user_profile.phone_number,
                    'image': self.user.user_profile.image.url if self.user.user_profile.image else None,
                    'facebook_link': self.user.user_profile.facebook_link,
                    'instagram_link': self.user.user_profile.instagram_link,
                    'tiktok_link': self.user.user_profile.tiktok_link,
                    'youtube_link': self.user.user_profile.youtube_link
                }
            }
        })

        return data
