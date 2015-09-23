__author__ = 'christian'

# coding=utf-8
"""FETI landing page view."""

__author__ = 'Christian Christelis <christian@kartoza.com>'
__date__ = '04/2015'
__license__ = "GPL"
__copyright__ = 'kartoza.com'

import os
from collections import OrderedDict
from haystack.query import SearchQuerySet
from haystack.inputs import AutoQuery

from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.template.loader import render_to_string
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.utils.translation import activate

from feti.models.campus import Campus
from feti.models.field_of_study import FieldOfStudy
from feti.models.campus_course_entry import CampusCourseEntry

from feti.models.campus import Campus


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


class Command(BaseCommand):
    help = 'Generate the full search result langing page.'

    def handle(self, *args, **options):
        def provider_key(item):
            return item[0].primary_institution.strip().lower()

        activate(settings.LANGUAGE_CODE)  # or any language code

        provider_dict = OrderedDict()
        campuses = Campus.objects.filter(_complete=True).order_by(
            '_long_description')
        for campus in campuses:
            if campus.incomplete:
                continue
            provider = campus.provider
            update_campus_dict(provider_dict, provider, campus)
            for course in campus.courses.all():
                update_course_dict(provider_dict[provider], campus, course)

        provider_dict = OrderedDict(
            sorted(provider_dict.items(), key=provider_key))

        for c in campuses:
            c.related_course = provider_dict[c.provider][c]

        # Add the navigation bar back
        # Sometimes a small hack is better than no hack ;)
        # Change this if you don't agree with the above statement...
        navigation_bar = '{% include "feti/navigation_bar.html" %}'
        context = {
            'navigation_bar': navigation_bar,
            'campuses': campuses,
            'provider_dict': provider_dict,
            'search_terms': '',
            'private_institutes': 'on',
            'errors': '',
            'fields_of_study': FieldOfStudy.objects.all().order_by(
                'field_of_study_description'),
            'field_of_study_id': 0
        }

        rendered_landing_page = render_to_string(
            'feti/feti.html',
            context)

        new_template_location = os.path.join(
            settings.TEMPLATE_DIRS[0],
            'feti_rendered.html')

        with open(new_template_location, 'w') as new_template:
            new_template.write(rendered_landing_page.encode("UTF-8"))

