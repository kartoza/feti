from rest_framework import serializers
from feti.models.provider import Provider

__author__ = 'irwan'


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
