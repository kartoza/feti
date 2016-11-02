from rest_framework import serializers
from feti.models.campus import Campus
from feti.serializers.course_serializer import CourseSerializer

__author__ = 'irwan'


class CampusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campus

    def to_representation(self, instance):
        res = super(CampusSerializer, self).to_representation(instance)
        course_context = {}

        res['saved'] = False
        if self.context.get("campus_saved"):
            try:
                fav = next(item for item in self.context.get("campus_saved") if item.campus.id == res['id'])
                res['saved'] = True
                course_context['course_saved'] = list(fav.courses.all().values_list('id', flat=True))
            except StopIteration:
                pass

        if self.context.get("courses"):
            res['courses'] = CourseSerializer(
                instance.courses.filter(id__in=self.context.get('courses')),
                many=True,
                context=course_context).data
        else:
            res['courses'] = CourseSerializer(
                instance.courses.all(),
                many=True,
                context=course_context).data

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
