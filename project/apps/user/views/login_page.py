from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views import View
from django.views.generic import TemplateView

from ..forms.login import LoginForm
from utils.mixins.auth import AuthenticatedMixin

class LoginPageView(TemplateView):
    template_name = 'pages/login/login.html'

    def get(self, request):
        form = LoginForm()
        return render(request, 'pages/login/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                if form.cleaned_data['remember_me']:
                    request.session.set_expiry(1209600)  # 2 weeks
                else:
                    request.session.set_expiry(0)

                # Check if 'next' URL parameter is present
                next_url = request.POST.get('next')
                if next_url:
                    return redirect(next_url)
                
                return redirect('home')
            else:
                form.add_error(None, 'Invalid email or password')
        return render(request, 'pages/login/login.html', {'form': form})
