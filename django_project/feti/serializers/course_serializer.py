import re
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
        title = instance.__unicode__()

        if self.context.get("course_saved"):
            if res['id'] in self.context.get("course_saved"):
                res['saved'] = True

        if self.context.get("query"):
            query_words = self.context.get("query")
            queries = query_words.split()
            title = re.sub(
                '(?i)(' + '|'.join(map(re.escape, queries)) + ')', r'<mark>\1</mark>',
                title
            )

        res['title'] = title
        res['model'] = 'course'
        return res
