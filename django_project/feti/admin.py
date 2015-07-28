# coding=utf-8
"""Model Admin Class."""

from django.contrib.gis import admin
from feti.models.address import Address
from feti.models.campus import Campus
from feti.models.course import Course
from feti.models.provider import Provider


class AddressAdmin(admin.ModelAdmin):
    """Admin Class for Address Model."""
    list_display = ('id', 'address_line_1', 'town', 'postal_code', 'phone',)
    list_filter = ['town', 'postal_code', ]
    search_fields = ['address_line_1', 'town', 'postal_code', 'phone', ]
    exclude = ('campus_fk', )


class AddressAdminInline(admin.StackedInline):
    """Stacked Inline Admin Class to be included in Campus Admin"""
    model = Address
    fk_name = 'campus_fk'


class CampusAdmin(admin.OSMGeoAdmin):
    """Admin Class for Campus Model."""
    inlines = [AddressAdminInline]
    list_display = ('campus', 'provider', '_complete',)
    list_filter = ['provider', '_complete']
    search_fields = ['campus', 'provider__primary_institution']
    exclude = ('_long_description', '_complete', '_campus_popup', 'address')


class ProviderAdmin(admin.ModelAdmin):
    """Admin Class for Provider Model."""
    list_display = ('primary_institution', 'website', 'status',)
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
    exclude = ('_long_description', '_course_popup')


admin.site.site_header = 'Feti Administration'
admin.site.site_title = 'Feti Administration'
admin.site.register(Campus, CampusAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Provider, ProviderAdmin)
admin.site.register(Course, CourseAdmin)
