from rest_framework import serializers
from feti.models.campus import Campus
from feti.serializers.course_serializer import CourseSerializer

__author__ = 'irwan'


class CampusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campus

    def to_representation(self, instance):
        res = super(CampusSerializer, self).to_representation(instance)

        res['saved'] = False
        if self.context.get("user_campuses"):
            if res['id'] in self.context.get("user_campuses"):
                res['saved'] = True

        if self.context.get("courses"):
            res['courses'] = CourseSerializer(
                instance.courses.filter(id__in=self.context.get('courses')), many=True).data
        else:
            res['courses'] = CourseSerializer(instance.courses.all(), many=True).data

        res['long_description'] = instance.long_description
        if instance.address:
            res['address'] = instance.address.__unicode__()
        if instance.provider:
            res['title'] = instance.provider.__unicode__()
        if instance.location:
            res['location'] = {
                'lat': instance.location.y,
                'lng': instance.location.x}
        res['model'] = 'campus'
        return res
