from django.views.generic import TemplateView

__author__ = 'Dimas Tri Ciputra'


class LandingPage(TemplateView):
    template_name = 'feti/landing_page.html'
