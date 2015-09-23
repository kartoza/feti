# coding=utf-8
"""FETI landing page view."""

__author__ = 'Christian Christelis <christian@kartoza.com>'
__date__ = '04/2015'
__license__ = "GPL"
__copyright__ = 'kartoza.com'

from collections import OrderedDict
from haystack.query import SearchQuerySet
from haystack.inputs import AutoQuery

from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext

from feti.models.campus import Campus
from feti.models.field_of_study import FieldOfStudy
from feti.models.campus_course_entry import CampusCourseEntry


def update_course_dict(campus_dict, campus, course):
    if campus not in campus_dict:
        campus_dict[campus] = [course]
    else:
        if course not in campus_dict[campus]:
            campus_dict[campus].append(course)


def update_campus_dict(provider_dict, provider, campus):
    if provider not in provider_dict:
        campus_dict = dict()
        campus_dict[campus] = []
        provider_dict[provider] = campus_dict
    else:
        if campus not in provider_dict[provider]:
            provider_dict[provider][campus] = []


def landing_page(request):
    """Serves the FETI landing page.

    :param request: A django request object.
    :type request: request

    :returns: Returns the landing page.
    :rtype: HttpResponse
    """
    # sort the campus alphabetically
    def provider_key(item):
        return item[0].primary_institution.strip().lower()

    search_terms = ''
    private_institutes = 'on'
    field_of_study_id = 0
    provider_dict = OrderedDict()
    errors = None
    campuses = []
    if request.GET:
        search_terms = request.GET.get('search_terms')
        private_institutes = request.GET.get('private_institutes') or 'off'
        field_of_study_id = request.GET.get('field_of_study_id') or 0
        try:
            field_of_study_id = int(field_of_study_id)
        except ValueError:
            field_of_study_id = 0
        if search_terms:

            results = SearchQuerySet().filter(
                text=AutoQuery(search_terms)).models(
                CampusCourseEntry)

            for result in results:
                if result.score > 2:
                    # get model
                    model = result.model
                    # get objects
                    object_instance = result.object

                    campus = object_instance.campus
                    if private_institutes == 'off':
                        if (
                                campus.provider.status ==
                                campus.provider.PROVIDER_STATUS_PRIVATE):
                            continue
                    if campus.incomplete:
                        continue

                    course = object_instance.course
                    if field_of_study_id:
                        if not course.field_of_study:
                            continue
                        if course.field_of_study.id != field_of_study_id:
                            continue

                    if campus not in campuses:
                        campuses.append(campus)

                    provider = campus.provider
                    update_campus_dict(provider_dict, provider, campus)
                    update_course_dict(
                        provider_dict[provider], campus, course)

    if not request.GET or not search_terms:
        return render(
            request,
            'feti_rendered.html')

    provider_dict = OrderedDict(
        sorted(provider_dict.items(), key=provider_key))

    for c in campuses:
        c.related_course = provider_dict[c.provider][c]

    context = {
        'campuses': campuses,
        'provider_dict': provider_dict,
        'search_terms': search_terms,
        'private_institutes': private_institutes,
        'errors': errors,
        'fields_of_study': FieldOfStudy.objects.all().order_by(
            'field_of_study_description'),
        'field_of_study_id': field_of_study_id
    }
    return render(
        request,
        'feti/feti.html',
        context_instance=RequestContext(request, context))
