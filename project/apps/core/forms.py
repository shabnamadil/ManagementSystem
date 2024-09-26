from django import forms

from .models import SiteSettings


class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = '__all__'

    def clean_number(self) -> str:
        number = self.cleaned_data.get('number', '')
        if number.startswith('+'):
            number_without_plus = number[1:]
        else:
            number_without_plus = number

        if number_without_plus and not number_without_plus.isdigit():
            raise forms.ValidationError('Only numeric values are allowed.')

        if number_without_plus and len(number_without_plus) < 10:
            raise forms.ValidationError('Mobile number must be at least 10 characters.')
        
        return number
