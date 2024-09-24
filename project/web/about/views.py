from django.views.generic import TemplateView

from apps.pages.about.models import AboutUs, Team


class AboutPageView(TemplateView):
    template_name = 'pages/about/index.html'

    def get_context_data(self, **kwargs):
        context = super(AboutPageView, self).get_context_data(**kwargs)
        context['about_us'] = AboutUs.load()
        context['team_members'] = Team.objects.all()
        # context["partners"] = Partner.objects.all()
        return context