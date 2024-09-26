from django.core.exceptions import ValidationError

from rest_framework import serializers

from ..models import Contact


class ContactPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = (
            'name',
            'surname',
            'email',
            'mobile_number',
            'message'
        )

    def validate(self, attrs):
        mobile_number = attrs.get('mobile_number', '')

        if mobile_number.startswith('+'):
            mobile_number_without_plus = mobile_number[1:]
        else:
            mobile_number_without_plus = mobile_number

        if mobile_number_without_plus and not mobile_number_without_plus.isdigit():
            raise ValidationError({'mobile_number': 'Only numeric values are allowed.'})
        if mobile_number_without_plus and len(mobile_number_without_plus) < 10:
            raise ValidationError({'mobile_number': 'Mobile number must be at least 10 characters.'})
        
        return super().validate(attrs)