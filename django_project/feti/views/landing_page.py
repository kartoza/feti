from django.views.generic import TemplateView

__author__ = 'Dimas Tri Ciputra'


class LandingPage(TemplateView):
    template_name = 'feti/landing_page.html'

    def get_context_data(self, **kwargs):
        context = super(LandingPage, self).get_context_data(**kwargs)
        context['next'] = '/'
        return context
