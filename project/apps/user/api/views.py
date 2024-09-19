from django.contrib.auth import get_user_model

from rest_framework.generics import (
    CreateAPIView
)

from .serializers import (
    RegisterSerializer
)

User = get_user_model()


class RegisterAPIView(CreateAPIView):
    serializer_class = RegisterSerializer