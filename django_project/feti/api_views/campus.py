from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from haystack.query import SearchQuerySet
from rest_framework.response import Response
from rest_framework.views import APIView
from feti.models.campus import Campus
from feti.serializers.campus_serializer import CampusSummarySerializer

__author__ = 'Dimas Ciputra <dimas@kartoza.com>'
__date__ = '16/01/17'


class AllCampus(APIView):
    """List all available campus."""

    def get(self, request):
        sqs = SearchQuerySet().filter(
            courses_is_null='false',
            campus_location_is_null='false'
        ).models(Campus)

        page = request.GET.get('page')

        campuses_in_page = 50

        paginator = Paginator(sqs, campuses_in_page)

        try:
            campuses = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            page = 1
            campuses = paginator.page(page)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            page = paginator.num_pages
            campuses = paginator.page(page)

        campus_data = []

        if campuses:
            for result in campuses:
                stored_fields = result.get_stored_fields()
                if stored_fields['campus_location']:
                    campus_location = stored_fields['campus_location']
                    stored_fields['campus_location'] = "{0},{1}".format(
                        campus_location.y, campus_location.x
                    )

                # Delete elements we don't need
                del stored_fields['campus_popup']
                del stored_fields['text']
                del stored_fields['courses']
                del stored_fields['campus_website']
                del stored_fields['campus_auto']
                del stored_fields['long_description']
                del stored_fields['courses_is_null']
                del stored_fields['campus_is_null']
                del stored_fields['campus_location_is_null']
                del stored_fields['provider_primary_institution']
                del stored_fields['campus_address']

                campus_data.append(stored_fields)

        data = {
            'campuses': campus_data,
            'page': paginator.num_pages,
            'current_page': page
        }

        return Response(data)


class CampusSummary(APIView):
    """Get detail of campus"""

    def get(self, request):
        campus_id = request.GET.get('id')

        if not campus_id:
            return Response(None)

        try:
            campus = Campus.objects.get(id=campus_id)
        except Campus.DoesNotExist:
            return Response(None)

        serializer = CampusSummarySerializer(campus)

        return Response(serializer.data)
