from django.views.generic import TemplateView

from apps.pages.home.models import Partner

class HomePageView(TemplateView):
    template_name = 'pages/home/index.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context["partners"] = Partner.objects.all()
        return context