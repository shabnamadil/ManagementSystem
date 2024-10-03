from rest_framework.generics import CreateAPIView

from .serializers import NewsletterPostSerializer


class NewsletterPostAPIView(CreateAPIView):
    serializer_class = NewsletterPostSerializer