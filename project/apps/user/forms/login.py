from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'name@example.com'}),
        label="Email address"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': '***************'}),
        label="Password"
    )
    remember_me = forms.BooleanField(required=False, label="Remember me")

    def add_class(self, class_name):
        for field in self.fields.values():
            field.widget.attrs['class'] = class_name
        return self
