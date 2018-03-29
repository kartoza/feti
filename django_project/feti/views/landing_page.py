import json

from django.conf import settings
from django.views.generic import TemplateView
from feti.models.course import Course
from feti.models.occupation import Occupation
from user_profile.models import CampusCoursesFavorite
from feti.serializers.favorite_serializer import BaseFavoriteSerializer
from ..prometheus_feti.counter import PrometheusCounter
from ..prometheus_feti.response_time import ResponseTimeMixin

__author__ = 'Dimas Tri Ciputra'


class LandingPage(PrometheusCounter, ResponseTimeMixin, TemplateView):
    template_name = 'feti/landing_page.html'

    def get_context_data(self, **kwargs):
        self.increase_landing_page_view()
        self.get_response_time(request = self.request)
        context = super(LandingPage, self).get_context_data(**kwargs)
        context['next'] = '/'
        context['courses'] = Course.objects.count()
        context['occupations'] = Occupation.objects.count()
        context['favorite'] = []
        context['limit_per_page'] = settings.LIMIT_PER_PAGE
        if self.request.user.is_authenticated():
            #  check save campus/course
            campus_course_fav = CampusCoursesFavorite.objects.filter(
                user=self.request.user)

            serializer = BaseFavoriteSerializer(campus_course_fav, many=True)
            context['favorite'] = json.dumps(serializer.data)
        return context


class EmbedPage(LandingPage):
    template_name = 'feti/embed_page.html'

    def get_context_data(self, **kwargs):
        context = super(EmbedPage, self).get_context_data(**kwargs)
        return context
