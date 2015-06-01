# coding=utf-8
"""FETI landing page view."""
from collections import OrderedDict
from feti.models.course import Course
from haystack.query import SearchQuerySet
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext

from feti.models.campus import Campus

__author__ = 'Christian Christelis <christian@kartoza.com>'
__date__ = '04/2015'
__license__ = "GPL"
__copyright__ = 'kartoza.com'


def landing_page(request):
    """Serves the FETI landing page.

    :param request: A django request object.
    :type request: request

    :returns: Returns the landing page.
    :rtype: HttpResponse
    """
    search_terms = ''
    campuses = Campus.objects.all()[:1500]
    course_dict = OrderedDict()
    errors = None
    if request.GET:
        search_terms = request.GET.get('search_terms')
        if search_terms:
            campuses = SearchQuerySet().filter(content=search_terms).models(
                Campus)
            courses = SearchQuerySet().filter(content=search_terms).models(
                Course)
            for campus in [c.object for c in campuses[:1500]]:
                course_dict[campus] = campus.courses.all()
            for course in [c.object for c in courses[:1500]]:
                for campus in course.campus_set.all():
                    if campus in course_dict:
                        if course not in course_dict[campus]:
                            course_dict[campus].append(course)
                    else:
                        course_dict[campus] = [course]
        else:
            for campus in [c for c in campuses[:1500]]:
                course_dict[campus] = campus.courses.all()
    else:
        for campus in [c for c in campuses[:1500]]:
            course_dict[campus] = campus.courses.all()

    # sort the campus alphabetically
    def campus_key(item):
        return '%s : %s' % (
            item[0].campus.provider.primary_institution,
            item[0].campus.strip().lower())
    course_dict = OrderedDict(sorted(course_dict.items(), key=campus_key))

    context = {
        'course_dict': course_dict,
        'search_terms': search_terms,
        'errors': errors
    }
    return render(
        request,
        'feti/feti.html',
        context_instance=RequestContext(request, context))
