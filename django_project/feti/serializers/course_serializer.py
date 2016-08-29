from rest_framework import serializers
from feti.models.course import Course
from feti.models.campus import Campus

__author__ = 'irwan'


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course

    def to_representation(self, instance):
        res = super(CourseSerializer, self).to_representation(instance)
        res['title'] = instance.__unicode__()
        locations = []
        for campus in Campus.objects.filter(courses=instance):
            if campus.location:
                locations.append(
                    {'lat': campus.location.y, 'lng': campus.location.x,
                     'popup': campus._campus_popup})
        res['locations'] = locations
        return res
