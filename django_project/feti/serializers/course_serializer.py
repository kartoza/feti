__author__ = 'irwan'

from rest_framework import serializers
from feti.models.course import Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
