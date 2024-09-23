from django.views.generic import TemplateView


class BlogPageView(TemplateView):
    template_name = 'pages/blog/index.html'

    def get_context_data(self, **kwargs):
        context = super(BlogPageView, self).get_context_data(**kwargs)
        return context