# coding=utf-8
"""FETI landing page view."""
from feti.models.course import Course
from feti.models.course_provider_link import CourseProviderLink
from haystack.query import SearchQuerySet

__author__ = 'Christian Christelis <christian@kartoza.com>'
__date__ = '04/2015'
__license__ = "GPL"
__copyright__ = 'kartoza.com'

from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext

from feti.models.campus import Campus
from feti.models.provider import Provider


def landing_page(request):
    """Serves the FETI landing page.

    :param request: A django request object.
    :type request: request

    :returns: Returns the landing page.
    :rtype: HttpResponse
    """
    search_terms = ''
    campuses = Campus.objects.all()
    courses = Course.objects.all()
    providers = Provider.objects.all()
    course_dict = dict()
    errors = None
    if request.POST:
        search_terms = request.POST.get('search_terms')
        campuses = SearchQuerySet().filter(content=search_terms).models(
            Campus)
        courses = SearchQuerySet().filter(content=search_terms).models(
            Course)
        for campus in [c.object for c in campuses]:
            course_dict[campus] = campus.linked_courses()
        for course in [c.object for c in courses]:
            linked_campuses = CourseProviderLink.objects.filter(
                course=course)
            for campus in [c.campus for c in linked_campuses]:
                if campus in course_dict:
                    if course not in course_dict[campus]:
                        course_dict[campus].append(course)
                else:
                    course_dict[campus] = [course]
    else:
        for campus in [c for c in campuses]:
            course_dict[campus] = campus.linked_courses()

    context = {
        'campuses': campuses,
        'providers': providers,
        'courses': courses,
        'course_dict': course_dict,
        'search_terms': search_terms,
        'errors': errors
    }
    return render(
        request,
        'feti/feti.html',
        context_instance=RequestContext(request, context))
