from django.views.generic import TemplateView


class FreelancerPageView(TemplateView):
    template_name = 'pages/freelancer/index.html'

    def get_context_data(self, **kwargs):
        context = super(FreelancerPageView, self).get_context_data(**kwargs)
        return context