# coding=utf-8
"""FETI landing page view."""
from haystack.inputs import AutoQuery

__author__ = 'Christian Christelis <christian@kartoza.com>'
__date__ = '04/2015'
__license__ = "GPL"
__copyright__ = 'kartoza.com'

from collections import OrderedDict
from haystack.query import SearchQuerySet

from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext

from feti.models.campus import Campus
from feti.models.course import Course


def landing_page(request):
    """Serves the FETI landing page.

    :param request: A django request object.
    :type request: request

    :returns: Returns the landing page.
    :rtype: HttpResponse
    """
    # sort the campus alphabetically
    def campus_key(item):
        return item[0].long_description.strip().lower()

    search_terms = ''
    course_dict = OrderedDict()
    errors = None
    if request.GET:
        search_terms = request.GET.get('search_terms')
        if search_terms:

            results = SearchQuerySet().filter(
                long_description=AutoQuery(search_terms)).models(Campus,
                                                                 Course)

            for result in results:
                if result.score > 1:
                    # get model
                    model = result.model
                    object = result.object
                    if model == Campus and isinstance(object, Campus):
                        campus = object
                        if campus.incomplete:
                            continue
                        course_dict[campus] = campus.courses.all()
                    if model == Course and isinstance(object, Course):
                        course = object
                        for campus in course.campus_set.all():
                            if campus in course_dict:
                                if course not in course_dict[campus]:
                                    course_dict[campus].append(course)
                            else:
                                course_dict[campus] = [course]
        else:
            campuses = Campus.objects.filter(_complete=True).order_by(
                '_long_description')
            for campus in campuses:
                course_dict[campus] = campus.courses.all()
    else:
        campuses = Campus.objects.filter(_complete=True).order_by(
            '_long_description')
        for campus in campuses:
            course_dict[campus] = campus.courses.all()

    course_dict = OrderedDict(
        sorted(course_dict.items(), key=campus_key))

    context = {
        'course_dict': course_dict,
        'search_terms': search_terms,
        'errors': errors
    }
    return render(
        request,
        'feti/feti.html',
        context_instance=RequestContext(request, context))
