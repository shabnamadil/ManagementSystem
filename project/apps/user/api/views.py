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

User = get_user_model()


class RegisterAPIView(CreateAPIView):
    serializer_class = RegisterSerializer


class VerifyOTP(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp_entered = request.data.get('otp')

        try:
            user = User.objects.get(email=email, otp=otp_entered)
            user.is_verified = True

            user.save()

            return Response({'message': 'Email verified successfully.'}, 
                              status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'detail': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)