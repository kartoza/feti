from rest_framework import serializers
from feti.utilities.highlighter import QueryHighlighter
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
            highlight = QueryHighlighter(self.context.get("query"))
            title = highlight.highlight(title)
            if instance.national_learners_records_database:
                title = title.replace('...', instance.national_learners_records_database + ' - ')
            else:
                title = title.replace('...', '')

        res['title'] = title
        res['model'] = 'course'
        return res
