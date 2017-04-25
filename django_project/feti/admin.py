# coding=utf-8
"""Model Admin Class."""

from django.contrib.gis import admin
from django.core.urlresolvers import reverse
from nested_inline.admin import NestedStackedInline, NestedModelAdmin, NestedTabularInline
from django.template.context import Context
from django.template.loader import get_template
from django.utils.safestring import mark_safe

from feti.custom_admin.geodjango import OSMGeoStackedInline
from feti.models.address import Address
from feti.models.campus import Campus
from feti.models.course import Course
from feti.models.field_of_study import FieldOfStudy
from feti.models.provider import Provider
from feti.models.occupation import Occupation
from feti.models.learning_pathway import LearningPathway, Step, StepDetail
from feti.models.url import URL
from feti.models.education_training_quality_assurance import EducationTrainingQualityAssurance
from feti.models.national_qualifications_framework import NationalQualificationsFramework
from feti.models.feedback import Feedback


class AddressAdmin(admin.ModelAdmin):
    """Admin Class for Address Model."""
    list_display = ('id', 'address_line_1', 'town', 'postal_code', 'phone',)
    list_filter = ['town', 'postal_code', ]
    readonly_fields = ['provider_url']
    search_fields = ['address_line_1', 'town', 'postal_code', 'phone', ]
    exclude = ('campus_fk',)

    def provider_url(self, instance):
        return mark_safe('{}<br/><a href="{}">Go to edit page</a>').format(
            instance.campus_fk.provider,
            reverse('admin:feti_provider_change', args=(
                instance.campus_fk.provider.id,)),
        )

    provider_url.allow_tags = True
    provider_url.short_description = 'Primary institute'


class AddressAdminInline(admin.StackedInline):
    """Stacked Inline Admin Class to be included in Campus Admin"""
    inline_classes = ('grp-collapse', 'grp-open')
    model = Address
    fk_name = 'campus_fk'
    max_num = 1
    extra = 0


class CampusAdmin(admin.OSMGeoAdmin):
    """Admin Class for Campus Model."""
    openlayers_url = '/static/feti/js/libs/OpenLayers-2.13.1/OpenLayers.js'
    inlines = [AddressAdminInline]
    list_display = ('id', 'campus', 'primary_institution', '_complete', '_campus_popup')
    list_filter = ['provider__primary_institution', '_complete']
    search_fields = ['campus', 'provider__primary_institution']
    readonly_fields = ['provider_url']
    fieldsets = (
        ('General Information', {
            'fields': ('provider_url', 'campus', 'location',
                       'courses', '_campus_popup')
        }),
    )
    exclude = ('_long_description', '_complete',
               'address', 'provider')
    filter_horizontal = ['courses']
    related_lookup_fields = {
        'fk': ['provider'],
        'm2m': ['courses']
    }

    def has_add_permission(self, request):
        # disable add permission so we always add this from providers menu
        return False

    def provider_url(self, instance):
        return mark_safe('{}<br/><a href="{}">Go to edit page</a>').format(
            instance.provider,
            reverse('admin:feti_provider_change', args=(
                instance.provider.id,)),
        )

    provider_url.allow_tags = True
    provider_url.short_description = 'Primary institute url'


class CampusAdminInline(OSMGeoStackedInline):
    """Inline Admin Class for campus"""
    model = Campus
    show_change_link = True
    inlines = [AddressAdminInline]
    extra = 0
    readonly_fields = ['campus_url']
    fieldsets = (
        (None, {
            'fields': ('campus', 'location', 'campus_url', 'courses')
        }),
    )
    list_display = ('campus', 'provider', '_complete',)
    list_filter = ['provider', '_complete']
    search_fields = ['campus', 'provider__primary_institution']
    exclude = ('_long_description', '_complete', '_campus_popup', 'address')
    filter_horizontal = ['courses']

    def campus_url(self, instance):
        return mark_safe('{}<br/><a href="{}">Go to Edit '
                         'page</a>').format(
            instance.address_fk.address_line,
            reverse('admin:feti_campus_change', args=(
                instance.id,))
        )

    campus_url.allow_tags = True
    campus_url.short_description = 'Address'


class ProviderAdmin(admin.OSMGeoAdmin):
    """Admin Class for Provider Model."""
    inlines = [CampusAdminInline]
    openlayers_url = '/static/feti/js/libs/OpenLayers-2.13.1/OpenLayers.js'

    fieldsets = (
        ('General', {
            'fields': ['primary_institution', 'website', 'status', 'icon']
        }),
    )
    list_display = ('id', 'primary_institution', 'website',)
    list_filter = ['primary_institution', 'website', ]
    search_fields = ['primary_institution', 'website', ]
    # exclude = ['status']


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
                     'course_description',
                     'education_training_quality_assurance__acronym',
                     'education_training_quality_assurance__body_name',
                     'national_qualifications_framework__description']
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


class StepInline(NestedTabularInline):
    model = Step
    extra = 1


class LearningPathwayline(NestedStackedInline):
    model = LearningPathway
    extra = 1
    inlines = [StepInline]


class OccupationAdmin(NestedModelAdmin):
    model = Occupation
    inlines = [LearningPathwayline]
    list_filter = ['green_occupation', 'scarce_skill', 'occupation_regulation']
    search_fields = ['occupation', 'tasks', 'learning_pathway_description']


class StepDetailAdmin(admin.ModelAdmin):
    model = StepDetail
    search_fields = ['title', 'detail']


class URLAdmin(admin.ModelAdmin):
    """Admin Class for URL Model."""
    list_display = ('url', 'random_string', 'date')
    list_filter = ['url', 'random_string', 'date']
    search_fields = ['url', 'random_string', 'date']
    readonly_fields = ('date', 'random_string')


admin.site.site_header = 'Feti Administration'
admin.site.site_url = '/'
admin.site.site_title = 'Feti Administration'
admin.site.register(Campus, CampusAdmin)
admin.site.register(Provider, ProviderAdmin)
admin.site.register(Course, CourseAdmin)

admin.site.register(Occupation, OccupationAdmin)
admin.site.register(StepDetail, StepDetailAdmin)
admin.site.register(Address, admin.ModelAdmin)
admin.site.register(FieldOfStudy, admin.ModelAdmin)
admin.site.register(URL, URLAdmin)

admin.site.register(EducationTrainingQualityAssurance)
admin.site.register(NationalQualificationsFramework)
admin.site.register(Feedback, admin.ModelAdmin)
