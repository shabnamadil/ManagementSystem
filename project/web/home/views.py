from django.views.generic import TemplateView

from apps.pages.home.models import (
    Partner, 
    HeroSection,
    HowToWork,
    Statistics
)
from apps.freelancer.models import FreelancerCategory

class HomePageView(TemplateView):
    template_name = 'pages/home/index.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context["partners"] = Partner.objects.all()
        context['hero_section'] = HeroSection.load()
        context['freelancer_categories'] = FreelancerCategory.objects.all()[:7]
        context['how_to_work'] = HowToWork.objects.all()[:4]
        context['statistics'] = Statistics.objects.all()[:4]
        return context