from django.views.generic import TemplateView


class DashboardPageView(TemplateView):
    template_name = 'pages/dashboard/test.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardPageView, self).get_context_data(**kwargs)
        return context