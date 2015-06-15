# coding=utf-8
"""Model Admin Class."""

from django.contrib.gis import admin
from feti.models.campus import Campus
from feti.models.address import Address
from feti.models.provider import Provider
from feti.models.course_provider_link import CourseProviderLink


class CampusAdmin(admin.OSMGeoAdmin):
    """Admin Class for Campus Model."""
    list_display = ('campus', 'location',)
    list_filter = ['campus', 'location',]
    search_fields = ['campus', 'location',]


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


class CourseProviderLinkAdmin(admin.ModelAdmin):
    """Admin Class for Address Model."""
    list_display = ('course', 'campus', )
    list_filter = ['course', 'campus', ]
    search_fields = ['course', 'campus', ]


admin.site.register(Campus, CampusAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Provider, ProviderAdmin)
admin.site.register(CourseProviderLink, CourseProviderLinkAdmin)
