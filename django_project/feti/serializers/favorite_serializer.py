from rest_framework import serializers
from feti.models.campus import Campus
from feti.serializers.course_serializer import CourseSerializer
from user_profile.models import CampusCoursesFavorite

__author__ = 'Dimas Ciputra <dimas@kartoza.com>'
__date__ = '02/11/16'


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampusCoursesFavorite
        fields = '__all__'

    def to_representation(self, instance):
        res = super(FavoriteSerializer, self).to_representation(instance)
        course_context = {}

        campus = instance.campus
        res['saved'] = True
        res['long_description'] = campus.long_description
        res['_campus_popup'] = campus.campus_popup
        res['campus'] = campus.campus
        res['id'] = campus.id
        if campus.address:
            res['address'] = campus.address.__unicode__()
        if campus.provider:
            res['title'] = campus.provider.__unicode__()
        if campus.location:
            res['location'] = {
                'lat': campus.location.y,
                'lng': campus.location.x}
        res['model'] = 'campus'
        course_context['course_saved'] = list(instance.courses.all().values_list('id', flat=True))
        res['courses'] = CourseSerializer(
            instance.courses.all(),
            many=True,
            context=course_context).data

        return res
