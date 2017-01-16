from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from haystack.query import SearchQuerySet
from rest_framework.response import Response
from rest_framework.views import APIView
from feti.models.campus import Campus

__author__ = 'Dimas Ciputra <dimas@kartoza.com>'
__date__ = '16/01/17'


class AllCampus(APIView):
    """List all available campus."""

    def get(self, request):
        sqs = SearchQuerySet().filter(
            courses_is_null='false',
            campus_location_is_null='false',
            campus_is_null='false'
        ).models(Campus)

        page = request.GET.get('page')

        campuses_in_page = 50

        paginator = Paginator(sqs, campuses_in_page)

        try:
            campuses = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            campuses = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            campuses = paginator.page(paginator.num_pages)

        campus_data = []

        if sqs:
            for result in campuses:
                stored_fields = result.get_stored_fields()
                if stored_fields['campus_location']:
                    campus_location = stored_fields['campus_location']
                    stored_fields['campus_location'] = "{0},{1}".format(
                        campus_location.y, campus_location.x
                    )
                campus_data.append(stored_fields)

        data = {
            'campuses': campus_data,
            'page': paginator.num_pages,
            'current_page': page
        }

        return Response(data)
