# coding=utf-8
"""Model Admin Class."""

from django.contrib.gis import admin
from django.core.urlresolvers import reverse
from django.forms.models import BaseInlineFormSet
from django.template.context import Context
from django.template.loader import get_template
from django.utils.html import format_html_join, format_html
from django.utils.safestring import mark_safe
from feti.custom_admin.geodjango import OSMGeoStackedInline
from feti.models.address import Address
from feti.models.campus import Campus
from feti.models.course import Course
from feti.models.provider import Provider


class AddressAdmin(admin.ModelAdmin):
    """Admin Class for Address Model."""
    list_display = ('id', 'address_line_1', 'town', 'postal_code', 'phone',)
    list_filter = ['town', 'postal_code', ]
    readonly_fields = ['campus_url', 'provider_url']
    search_fields = ['address_line_1', 'town', 'postal_code', 'phone', ]
    exclude = ('campus_fk', )

    def campus_url(self, instance):
        return mark_safe('{}<br/><a href="{}">Go to edit page</a>').format(
            instance.campus_fk,
            reverse('admin:feti_campus_change', args=(
                instance.campus_fk.id,)),
        )
    campus_url.allow_tags = True
    campus_url.short_description = 'Campus'

    def provider_url(self, instance):
        return mark_safe('{}<br/><a href="{}">Go to edit page</a>').format(
            instance.campus_fk.provider,
            reverse('admin:feti_campus_change', args=(
                instance.campus_fk.provider.id,)),
        )
    provider_url.allow_tags = True
    provider_url.short_description = 'Provider'


class AddressAdminInline(admin.StackedInline):
    """Stacked Inline Admin Class to be included in Campus Admin"""
    model = Address
    fk_name = 'campus_fk'
    max_num = 1
    extra = 0


class CampusAdmin(admin.OSMGeoAdmin):
    """Admin Class for Campus Model."""
    inlines = [AddressAdminInline]
    list_display = ('campus', 'provider', '_complete',)
    list_filter = ['provider', '_complete']
    search_fields = ['campus', 'provider__primary_institution']
    readonly_fields = ['provider_url']
    fieldsets = (
        ('General Information', {
            'fields': ('provider_url', 'provider', 'campus', 'location',
                       'courses')
        }),
    )
    exclude = ('_long_description', '_complete',
               '_campus_popup', 'address')
    filter_horizontal = ['courses']
    related_lookup_fields = {
        'fk': ['provider'],
        'm2m': ['courses']
    }

    def provider_url(self, instance):
        return mark_safe('{}<br/><a href="{}">Go to edit page</a>').format(
            instance.provider,
            reverse('admin:feti_provider_change', args=(
                instance.provider.id,)),
        )
    provider_url.allow_tags = True
    provider_url.short_description = 'Provider'


class CampusAdminInline(OSMGeoStackedInline):
    """Inline Admin Class for campus"""
    model = Campus
    show_change_link = True
    inlines = [AddressAdminInline]
    extra = 0
    readonly_fields = ['address_url']
    fieldsets = (
        (None, {
            'fields': ('campus', 'location', 'address_url', 'courses')
        }),
    )
    list_display = ('campus', 'provider', '_complete',)
    list_filter = ['provider', '_complete']
    search_fields = ['campus', 'provider__primary_institution']
    exclude = ('_long_description', '_complete', '_campus_popup', 'address')
    filter_horizontal = ['courses']

    def address_url(self, instance):
        return mark_safe('{}<br/><a href="{}">Go to Edit '
                         'page</a>').format(
            instance.address_fk.address_line,
            reverse('admin:feti_address_change', args=(
                instance.address_fk.id,))
        )
    address_url.allow_tags = True
    address_url.short_description = 'Address'


class ProviderAdmin(admin.OSMGeoAdmin):
    """Admin Class for Provider Model."""
    inlines = [CampusAdminInline]
    fieldsets = (
        ('General', {
            'fields': ['primary_institution', 'website']
        }),
    )
    list_display = ('primary_institution', 'website', 'status',)
    list_filter = ['primary_institution', 'website', 'status', ]
    search_fields = ['primary_institution', 'website', 'status', ]
    exclude = ['status']


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
    readonly_fields = ['related_providers']

    def related_providers(self, instance):
        template = get_template('admin/related_providers.html')
        providers = []
        for c in instance.campus_set.all():
            if c.provider not in providers:
                providers.append(c.provider)
        context = Context({
            'providers': providers
        })
        return mark_safe(template.render(context).replace('\n', ''))
    related_providers.allow_tags = True
    related_providers.short_description = 'Related providers'


admin.site.site_header = 'Feti Administration'
admin.site.site_url = '/'
admin.site.site_title = 'Feti Administration'
admin.site.register(Address, AddressAdmin)
admin.site.register(Provider, ProviderAdmin)
admin.site.register(Course, CourseAdmin)
