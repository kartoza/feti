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

        drawn_polygon = self.context.get('drawn_polygon')

        if drawn_polygon:
            campuses = Campus.objects.filter(
                courses=instance,
                location__within=drawn_polygon
            )
        else:
            campuses = Campus.objects.filter(courses=instance)

        for campus in campuses:
            if campus.location:
                locations.append(
                    {'lat': campus.location.y, 'lng': campus.location.x,
                     'popup': campus._campus_popup})
        res['locations'] = locations

        return res


class SimpleCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
