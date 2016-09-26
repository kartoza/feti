from rest_framework import serializers
from feti.models.course import Course

__author__ = 'irwan'


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course

    def to_representation(self, instance):
        res = super(CourseSerializer, self).to_representation(instance)
        res['title'] = instance.__unicode__()
        res['model'] = 'course'
        return res
