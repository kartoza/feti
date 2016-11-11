from rest_framework import serializers
from feti.models.learning_pathway import StepDetail

__author__ = 'irwan'


class StepDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = StepDetail

    def to_representation(self, instance):
        res = super(StepDetailSerializer, self).to_representation(instance)
        if instance.course.all():
            res['course_detail'] = []
            for course in instance.course.all():
                data = {
                    'saqa_id': course.national_learners_records_database,
                    'title': course.course_description
                }
                res['course_detail'].append(data)
        return res
