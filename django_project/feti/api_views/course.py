from rest_framework.response import Response
from rest_framework.views import APIView
from feti.models.course import Course

__author__ = 'Dimas Ciputra <dimas@kartoza.com>'
__date__ = '19/01/17'


class ApiCourseIds(APIView):
    """List all course description by Ids"""

    def get(self, request):

        ids = request.GET.get('ids')

        if ids:
            ids = ids.split(',')

        if not ids:
            return Response(None)

        courses = Course.objects.filter(id__in=ids)

        response_data = []

        for course in courses:
            if course:
                response_data.append({
                    'id': course.id,
                    'nlrd': course.national_learners_records_database,
                    'description': course.course_description
                })

        return Response(response_data)
