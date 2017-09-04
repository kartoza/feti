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
        query_dict = self.request.GET.dict()
        query, options = self.process_request(query_dict)

        if '=' in query:
            queries = query.split('=')
            # search by saqa id
            if 'saqa_id' in queries[0] and len(queries) > 1:
                saqa_ids = queries[1].split(',')
                return Response(self.filter_by_saqa_ids(saqa_ids, options))

        sqs = self.filter_by_course(query)

        sqs = self.advanced_filter(sqs, options)

        if options and 'shape' in options:
            if options['type'] == 'polygon':
                sqs = self.filter_polygon(sqs, options['shape'])
            elif options['type'] == 'circle':
                sqs = self.filter_radius(
                    sqs,
                    options['shape'],
                    options['radius']
                )

        campus_data = []

        if sqs:
            for result in sqs:
                stored_fields = result.get_stored_fields()
                if stored_fields['campus_location']:
                    campus_location = stored_fields['campus_location']
                    stored_fields['campus_location'] = "{0},{1}".format(
                        campus_location.y, campus_location.x
                    )
                del stored_fields['courses_isnull']
                del stored_fields['campus_location_isnull']

                campus_data.append(stored_fields)

        return Response(campus_data)


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
