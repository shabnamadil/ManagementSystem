from django.views.generic import TemplateView


class AboutPageView(TemplateView):
    template_name = 'pages/about/index.html'

    def get_context_data(self, **kwargs):
        context = super(AboutPageView, self).get_context_data(**kwargs)
        # context["partners"] = Partner.objects.all()
        return context