# coding=utf-8
"""Model Admin Class."""

from django.contrib.gis import admin
from feti.models.campus import Campus
from feti.models.address import Address
from feti.models.course import Course
from feti.models.provider import Provider
from feti.models.course_provider_link import CourseProviderLink


class CampusAdmin(admin.OSMGeoAdmin):
    """Admin Class for Campus Model."""
    list_display = ('campus', '_complete',)
    list_filter = ['campus', '_complete',]
    search_fields = ['campus',]
    exclude = ('_long_description', '_complete')


class AddressAdmin(admin.ModelAdmin):
    """Admin Class for Address Model."""
    list_display = ('address_line_1', 'postal_code', 'phone', )
    list_filter = ['address_line_1', 'postal_code', 'phone', ]
    search_fields = ['address_line_1', 'postal_code', 'phone', ]


class ProviderAdmin(admin.ModelAdmin):
    """Admin Class for Provider Model."""
    list_display = ('primary_institution', 'website', 'status', )
    list_filter = ['primary_institution', 'website', 'status', ]
    search_fields = ['primary_institution', 'website', 'status', ]


class CourseAdmin(admin.ModelAdmin):
    """Admin Class for Courses Model."""
    list_display = ('national_learners_records_database',
                    'course_description',
                    'education_training_quality_assurance',
                    'national_qualifications_framework',
                    'national_graduate_school_in_education',
                    'national_certificate_vocational',
                    'field_of_study')
    list_filter = ['education_training_quality_assurance',
                   'national_qualifications_framework',
                   'national_graduate_school_in_education',
                   'national_certificate_vocational',
                   'field_of_study']
    search_fields = ['national_learners_records_database',
                     'course_description']
    exclude = ('_long_description',)


admin.site.register(Campus, CampusAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Provider, ProviderAdmin)
admin.site.register(Course, CourseAdmin)
