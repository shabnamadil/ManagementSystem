from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView
)

from .serializers import (
    RegisterSerializer
)
from apps.user.models.otp import OTP
from utils.otp.generate_otp import generate_otp
from utils.otp.send_otp import send_otp_email

User = get_user_model()


class RegisterAPIView(CreateAPIView):
    serializer_class = RegisterSerializer


class VerifyOTPView(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp_entered = request.data.get('otp')

        try:
            user = User.objects.get(email=email)
            otp_instance = OTP.objects.get(user=user, otp=otp_entered, is_used=False)

            if otp_instance.is_valid():
                user.is_verified = True
                user.is_active = True

                otp_instance.is_used = True
                otp_instance.save()
                user.save()

                return Response({'message': 'Email verified successfully.'}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'OTP has expired or has already been used.'}, status=status.HTTP_400_BAD_REQUEST)
                
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        except OTP.DoesNotExist:
            return Response({'detail': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)
        

class ResendOtpView(APIView):
    def post(self, request):
            email = request.data.get('email')

            try:
                user = User.objects.get(email=email)
                if not user.is_verified:
                    otp_instance = generate_otp(user)
                    send_otp_email(user.email, otp_instance)
                    return Response({'message': 'OTP sent successfully.'}, status=status.HTTP_200_OK)
                return Response({'detail': 'User has already been verified.'}, status=status.HTTP_404_NOT_FOUND)
            
            except User.DoesNotExist:
                return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)