from rest_framework.response import Response
from rest_framework.views import APIView

from feti.api_views.common_search import CommonSearch

__author__ = 'Dimas Ciputra <dimas@kartoza.com>'
__date__ = '13/02/17'
__license__ = "GPL"
__copyright__ = 'kartoza.com'


class CourseAPIView(CommonSearch, APIView):
    """
    Api to filter course by query
    """
    def get(self, request, format=None):
        query, options = self.process_request(self.request.GET.dict())

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

