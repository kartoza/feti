from rest_framework import serializers
from feti.models.course import Course

__author__ = 'irwan'


class CourseSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('is_named_bar')

    def is_named_bar(self, course):
        return course.__unicode__()

    class Meta:
        model = Course
