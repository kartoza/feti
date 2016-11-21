from rest_framework import serializers
from feti.models.learning_pathway import StepDetail

__author__ = 'irwan'


class StepDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = StepDetail
        fields = '__all__'

    def to_representation(self, instance):
        res = super(StepDetailSerializer, self).to_representation(instance)
        if not instance.course.all():
            return res

        course_details = []
        for course in instance.course.all():

            title_exists = [i for i, v in
                            enumerate(course_details)
                            if v['title'] == course.course_description]

            if title_exists:
                course_detail = course_details[title_exists[0]]
                course_detail['saqa_id'] = course_detail['saqa_id'] + ',' + \
                                           course.national_learners_records_database

            else:
                data = {
                    'saqa_id': course.national_learners_records_database,
                    'title': course.course_description
                }
                course_details.append(data)

        res['course_detail'] = course_details
        return res
