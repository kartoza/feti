import json
from django.views.generic import TemplateView
from feti.models.course import Course
from feti.models.occupation import Occupation
from user_profile.models import CampusCoursesFavorite
from feti.serializers.favorite_serializer import BaseFavoriteSerializer

__author__ = 'Dimas Tri Ciputra'


class LandingPage(TemplateView):
    template_name = 'feti/landing_page.html'

    def get_context_data(self, **kwargs):
        context = super(LandingPage, self).get_context_data(**kwargs)
        context['next'] = '/'
        context['courses'] = Course.objects.count()
        context['occupations'] = Occupation.objects.count()
        context['favorite'] = []
        if self.request.user.is_authenticated():
            #  check save campus/course
            campus_course_fav = CampusCoursesFavorite.objects.filter(
                user=self.request.user)

            serializer = BaseFavoriteSerializer(campus_course_fav, many=True)
            context['favorite'] = json.dumps(serializer.data)
        return context
