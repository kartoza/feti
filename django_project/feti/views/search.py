# coding=utf-8
from datetime import date
from django.http import HttpResponse
from feti.models.campus import Campus
from feti.serializers.campus_serializer import CampusSerializer
from haystack.generic_views import SearchView

__author__ = 'Rizky Maulana Nugraha "lucernae" <lana.pcfre@gmail.com>'
__date__ = '24/04/15'


class MySearchView(SearchView):
    """My custom search view."""

    def get_queryset(self):
        queryset = super(MySearchView, self).get_queryset()
        # further filter queryset based on some set of criteria
        return queryset.filter(pub_date__gte=date(2015, 1, 1))

    def get_context_data(self, *args, **kwargs):
        context = super(MySearchView, self).get_context_data(*args, **kwargs)
        # do something
        return context


def search(request):
    if request.method == "POST":
        mode = request.POST.get('mode')
        q = request.POST.get('q')
        # get query
        if mode == 'provider':
            set = Campus.objects.filter(campus__contains=q)
            serializer = CampusSerializer(set, many=True)
            return HttpResponse(serializer.data, content_type='application/json')

        return HttpResponse("", content_type='application/json')
