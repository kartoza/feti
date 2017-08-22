from rest_framework.response import Response
from rest_framework.views import APIView

from feti.api_views.common_search import CommonSearch
from django.conf import settings

__author__ = 'Dimas Ciputra <dimas@kartoza.com>'
__date__ = '13/02/17'
__license__ = "GPL"
__copyright__ = 'kartoza.com'


class ApiCampus(CommonSearch, APIView):
    """
    Api to filter campus by query
    """
    def get(self, request, *args):
        """Get the campuses.

        :param request: HTTP request object
        :type request: HttpRequest

        :param args: Positional arguments
        :type args: tuple
        
        :returns: URL
        :rtype: HttpResponse
        """
        query_dict = self.request.GET.dict()
        if 'administrative' not in query_dict:
            if settings.ADMINISTRATIVE:
                query_dict['administrative'] = settings.ADMINISTRATIVE
        query, options = self.process_request(query_dict)
        campus_data = self.get_campuses(query, options)
        return Response(campus_data)

    def get_campuses(self, query, options):
        """Get campuses based on query and other filters."""
        search_in_campus_model = True

        if options['advance_search']:
            search_in_campus_model = False

            sqs = self.filter_indexed_campus_course(query)
            sqs = self.advanced_filter(sqs, options)
        else:
            sqs = self.filter_indexed_campus(query)

        if options and 'shape' in options:
            if options['type'] == 'polygon':
                sqs = self.filter_polygon(
                        sqs,
                        options['shape']
                )
            elif options['type'] == 'circle':
                sqs = self.filter_radius(
                        sqs,
                        options['shape'],
                        options['radius']
                )

        campus_data = []
        campuses = {}

        if not sqs:
            return Response(None)

        for result in sqs:
            stored_fields = result.get_stored_fields()
            if search_in_campus_model:
                if stored_fields['campus_location']:
                    campus_location = stored_fields['campus_location']
                    stored_fields['campus_location'] = "{0},{1}".format(
                            campus_location.y, campus_location.x
                    )

                # Remove uneeded fields
                del stored_fields['courses_is_null']
                del stored_fields['campus_is_null']
                del stored_fields['campus_location_is_null']
                del stored_fields['courses_id']
                del stored_fields['provider_primary_institution']
                del stored_fields['campus_auto']
                del stored_fields['long_description']
                del stored_fields['text']
                del stored_fields['campus_popup']

                campus_data.append(stored_fields)
            else:
                if stored_fields['campus_location']:
                    campus_location = stored_fields['campus_location']
                    stored_fields['campus_location'] = "{0},{1}".format(
                            campus_location.y, campus_location.x
                    )

                if stored_fields['campus_id'] not in campuses:
                    campuses[stored_fields['campus_id']] = []

                campuses[stored_fields['campus_id']].append(stored_fields)

        if campuses:
            for key, value in campuses.items():
                campus_object = dict()
                campus_object['campus_id'] = key
                campus_object['campus_location'] = value[0]['campus_location']
                campus_object['campus_provider'] = value[0]['campus_provider']
                campus_object['campus_address'] = value[0]['campus_address']
                campus_object['campus'] = value[0]['campus_campus']
                campus_object['campus_icon_url'] = value[0]['campus_icon']
                campus_object['campus_website'] = value[0]['campus_website']
                campus_object['campus_public_institution'] = value[0]['campus_public_institution']

                courses = []

                for course in value:
                    courses.append(
                            '%s ;; [%s] %s' % (
                                course['course_id'],
                                course['course_nlrd'],
                                course['course_course_description'].replace('\'', '\"')
                            )
                    )
                campus_object['courses'] = str(courses)
                campus_data.append(campus_object)

        return campus_data
