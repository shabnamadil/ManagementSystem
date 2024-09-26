from django import forms

from .models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = (
            'name',
            'surname',
            'email',
            'mobile_number',
            'message'
        )

    def clean_mobile_number(self) -> str:
        mobile_number = self.cleaned_data.get('mobile_number', '')
        if mobile_number.startswith('+'):
            mobile_number_without_plus = mobile_number[1:]
        else:
            mobile_number_without_plus = mobile_number

        if mobile_number_without_plus and not mobile_number_without_plus.isdigit():
            raise forms.ValidationError('Only numeric values are allowed.')

        if mobile_number_without_plus and len(mobile_number_without_plus) < 10:
            raise forms.ValidationError('Mobile number must be at least 10 characters.')
        
        return mobile_number_without_plus