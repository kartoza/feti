from rest_framework.response import Response
from rest_framework.views import APIView

from feti.api_views.common_search import CommonSearch
from feti.models.course import Course

__author__ = 'Dimas Ciputra <dimas@kartoza.com>'
__date__ = '13/02/17'
__license__ = "GPL"
__copyright__ = 'kartoza.com'


class CourseAPIView(CommonSearch, APIView):
    """
    Api to filter course by query
    """

    def get(self, request, format=None):
        """Get the courses.

        :param request: HTTP request object
        :type request: HttpRequest

        :param args: Positional arguments
        :type args: tuple

        :returns: URL
        :rtype: HttpResponse
        """

        query_dict = self.request.GET.dict()
        query, options = self.process_request(query_dict)
        course_data = self.search_courses(query, options)
        return Response(course_data)


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
