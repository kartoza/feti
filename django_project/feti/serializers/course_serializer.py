from rest_framework import serializers
from feti.models.course import Course

__author__ = 'irwan'


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

    def to_representation(self, instance):
        res = super(CourseSerializer, self).to_representation(instance)
        res['saved'] = False
        if self.context.get("course_saved"):
            if res['id'] in self.context.get("course_saved"):
                res['saved'] = True
        res['title'] = instance.__unicode__()
        res['model'] = 'course'
        return res
