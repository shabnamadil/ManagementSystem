from rest_framework.generics import CreateAPIView

from .serializers import ContactPostSerializer


class ContactPostAPIView(CreateAPIView):
    serializer_class = ContactPostSerializer