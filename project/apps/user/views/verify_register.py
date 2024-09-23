from django.views.generic import TemplateView



class VerifyRegisterPageView(TemplateView):
    template_name = 'pages/register/verify-register.html'