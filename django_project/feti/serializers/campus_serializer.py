from rest_framework import serializers
from feti.models.campus import Campus
from feti.models.course import Course
from feti.utilities.highlighter import QueryHighlighter
from feti.serializers.course_serializer import CourseSerializer

__author__ = 'irwan'


class CampusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campus
        fields = '__all__'

    def to_representation(self, instance):
        res = super(CampusSerializer, self).to_representation(instance)
        course_context = {}
        title = None
        icon = None
        if instance.provider:
            title = instance.provider.__unicode__()
            if instance.provider.icon:
                icon = instance.provider.icon.path[9:]

        res['saved'] = False
        if self.context.get("campus_saved"):
            for item in self.context.get("campus_saved"):
                if item.campus.id == res['id']:
                    res['saved'] = True
                    course_context['course_saved'] = list(item.courses.all().values_list('id', flat=True))

        if self.context.get("courses"):
            course_context['query'] = self.context.get("query")
            # order courses
            pk_name = ('id' if not getattr(Course._meta, 'pk', None)
                       else Course._meta.pk.name)
            pk_name = '%s.%s' % (Course._meta.db_table, pk_name)
            clauses = ' '.join(
                ['WHEN %s=\'%s\' THEN %s' % (pk_name, pk, i)
                 for i, pk in enumerate(self.context.get("courses"))]
            )
            ordering = 'CASE %s END' % clauses
            res['courses'] = CourseSerializer(
                instance.courses.filter(
                    id__in=self.context.get('courses')
                ).extra(
                    select={'ordering': ordering}, order_by=('ordering',)
                ),
                many=True,
                context=course_context).data
        else:
            res['courses'] = CourseSerializer(
                instance.courses.all(),
                many=True,
                context=course_context).data
            # Highlight campus
            highlight = QueryHighlighter(self.context.get("query"))
            if title:
                title = highlight.highlight(title)

        res['long_description'] = instance.long_description
        res['title'] = title
        res['icon'] = icon
        if instance.address:
            res['address'] = instance.address.__unicode__()
        if instance.location:
            res['location'] = {
                'lat': instance.location.y,
                'lng': instance.location.x}
        res['model'] = 'campus'
        return res
