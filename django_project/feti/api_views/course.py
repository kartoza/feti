from rest_framework.response import Response
from rest_framework.views import APIView

from feti.api_views.common_search import CampusSearch

__author__ = 'Dimas Ciputra <dimas@kartoza.com>'
__date__ = '13/02/17'
__license__ = "GPL"
__copyright__ = 'kartoza.com'


class CourseAPIView(CampusSearch, APIView):
    """
    Api to filter course by query
    """
    def get(self, request, format=None):
        query, options = self.process_request(request)

        sqs = self.filter_by_course(query)

        if options and 'advance_search' in options:
            if 'fos' in options:
                sqs = self.filter_fos(sqs, options['fos'])
            if 'sos' in options:
                sqs = self.filter_sos(sqs, options['sos'])
            if 'qt' in options:
                sqs = self.filter_qualification_type(sqs, options['qt'])
            if 'mc' in options:
                sqs = self.filter_minimum_credits(sqs, options['mc'])
            if 'nqf' in options:
                sqs = self.filter_nqf(sqs, options['nqf'])
            if 'nqsf' in options:
                sqs = self.filter_nqsf(sqs, options['nqsf'])

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
