from rest_framework import serializers
from feti.models.campus import Campus
from feti.serializers.course_serializer import CourseSerializer

__author__ = 'irwan'


class CampusSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('is_named_bar')

    def is_named_bar(self, campus):
        return campus.__unicode__()

    class Meta:
        model = Campus

    def to_representation(self, instance):
        res = super(CampusSerializer, self).to_representation(instance)
        res['long_description'] = instance.long_description
        res['courses'] = CourseSerializer(instance.courses.all(), many=True).data
        if instance.address:
            res['address'] = instance.address.__unicode__()
        if instance.provider:
            res['provider'] = instance.provider.__unicode__()
        return res
