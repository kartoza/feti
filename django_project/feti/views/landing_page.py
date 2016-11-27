from django.views.generic import TemplateView
from feti.models.course import Course
from feti.models.occupation import Occupation

__author__ = 'Dimas Tri Ciputra'


class LandingPage(TemplateView):
    template_name = 'feti/landing_page.html'

    def get_context_data(self, **kwargs):
        context = super(LandingPage, self).get_context_data(**kwargs)
        context['next'] = '/'
        context['courses'] = len(Course.objects.all())
        context['occupations'] = len(Occupation.objects.all())
        return context
