from rest_framework import serializers

from ..models import Newsletter


class NewsletterPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = (
            'id',
            'email'
        )