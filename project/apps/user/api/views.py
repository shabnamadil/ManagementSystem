from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from django.contrib.auth.forms import PasswordResetForm

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)
from rest_framework_simplejwt.token_blacklist.models import (
    OutstandingToken, 
    BlacklistedToken
)

from .serializers import (
    RegisterSerializer,
    UserUpdateDestroySerializer,
    PasswordResetSerializer,
    CustomTokenObtainPairSerializer
)
from .permissions import (
    IsUserOrReadOnly
)
from apps.user.models.otp import OTP
from ..tasks import send_registration_otp


User = get_user_model()


class RegisterAPIView(CreateAPIView):
    serializer_class = RegisterSerializer


class VerifyOTPView(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp_entered = request.data.get('otp')

        if not email or not otp_entered:
            return Response({'otp': _('Email and OTP are required.')}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
            otp_instance = OTP.objects.filter(user=user, is_used=False).order_by('-created_at').first()

            if not otp_instance:
                return Response({'otp': _('No valid OTP found for this user.')}, status=status.HTTP_400_BAD_REQUEST)

            if otp_instance.otp != otp_entered:
                return Response({'otp': _('The OTP you entered is incorrect.')}, status=status.HTTP_400_BAD_REQUEST)

            if not otp_instance.is_valid():
                return Response({'otp': _('OTP has expired or has already been used.')}, status=status.HTTP_400_BAD_REQUEST)
            
            otp_instance.is_used = True
            user.is_verified = True
            user.is_active = True

            otp_instance.save()
            user.save()

            return Response({'message': _('Email verified successfully.')}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'otp': _('User not found.')}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'otp': _('An error occurred: {}').format(str(e))}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class ResendOtpView(APIView):
    def post(self, request):
            email = request.data.get('email')

            try:
                user = User.objects.get(email=email)
                if not user.is_verified:
                    send_registration_otp.delay(user.email)
                    return Response({'message': _('OTP sent successfully.')}, status=status.HTTP_200_OK)
                return Response({'detail': _('User has already been verified.')}, status=status.HTTP_404_NOT_FOUND)
            
            except User.DoesNotExist:
                return Response({'detail': _('User not found.')}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            

class UserRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserUpdateDestroySerializer
    queryset = User.objects.filter(is_active=True, is_verified=True, is_banned=False)
    permission_classes = (IsAuthenticated, IsUserOrReadOnly)

    def get_object(self):
        obj = super().get_object()
        self.check_object_permissions(self.request, obj)
        return obj


class PasswordResetAPIView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            form = PasswordResetForm(data={'email': email})
            user_obj = User.objects.filter(email__iexact=email).first()

            if form.is_valid():
                if user_obj:
                    form.save(request=request)
                    return Response({'detail': 'Password reset email has been sent.'})
                else :
                    return Response({'detail': 'You have not registered yet'})
            else:
                return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class LogoutAPIView(APIView):
    permission_classes = (IsAuthenticated, IsUserOrReadOnly)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LogoutAllDevicesAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)
        return Response(status=status.HTTP_205_RESET_CONTENT)
    

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer