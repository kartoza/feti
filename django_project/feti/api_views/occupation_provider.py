# coding=utf-8
__author__ = 'Anita Hapsari <anita@kartoza.com>'
__date__ = '16/07/18'

from rest_framework.views import APIView, Response
from haystack.query import SearchQuerySet, SQ
from feti.models.occupation import Occupation
from feti.models.campus_course_entry import CampusCourseEntry
from feti.models.learning_pathway import Step
from feti.serializers.campus_serializer import CampusSummarySerializer


class ApiOccupationCampus(APIView):
    def get(self, request):
        id_query = request.GET.get('id')

        try:
            query = Occupation.objects.get(id=id_query)
            learning_path = \
                Step.objects.filter(learning_pathway__occupation=query)
            steps = [r.step_detail for r in learning_path]
            courses = [q.course.all() for q in steps]
            qs_courses = SQ()
            for course in courses:
                if len(course) != 0:
                    for course_item in course:
                        qs_courses.add(
                            SQ(course_course_description=
                               course_item.course_description), SQ.OR)
            if len(qs_courses) == 0:
                return Response({'Status': 'No courses found'})
        except Occupation.DoesNotExist:
            return Response({'query': 'DoesNotExist'})

        sqs = SearchQuerySet()
        results = sqs.filter(qs_courses).models(CampusCourseEntry)
        data = [r.object for r in results]
        campus = [i.campus for i in data]
        serializer = CampusSummarySerializer(campus, many=True)
        return Response(serializer.data)
