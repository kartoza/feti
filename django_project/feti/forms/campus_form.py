from django.contrib.gis import forms
from django.http import Http404
from feti.models.campus import Campus
from feti.models.course import Course
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout,
    Fieldset,
    Submit,
    Field,
)
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.gis import gdal
from django.contrib.gis.forms.widgets import BaseGeometryWidget

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '09/08/16'
__license__ = "GPL"
__copyright__ = 'kartoza.com'


class CustomOSMWidget(BaseGeometryWidget):
    """
    An OpenLayers/OpenStreetMap-based widget.
    """
    template_name = 'gis/openlayers-osm.html'
    default_lon = 5
    default_lat = 47

    class Media:
        css = {'all': ['admin/css/widgets.css', '/static/grappelli/jquery/ui/jquery-ui.min.css',
                       '/static/grappelli/stylesheets/screen.css']}
        js = (
            '/custom_admin/jsi18n',
            '/static/grappelli/jquery/jquery-2.1.4.min.js',
            '/static/grappelli/jquery/ui/jquery-ui.min.js',
            '/static/grappelli/js/grappelli.js',
            '/static/feti/js/libs/grappelli_override.js',
            '/static/admin/js/SelectBox.js',
            '/static/admin/js/SelectFilter2.js',
            '/static/feti/js/libs/OpenLayers-2.13.1/OpenLayers.js',
            '/static/feti/js/libs/OpenLayers-2.13.1/OpenStreetMapSSL.js',
            'gis/js/OLMapWidget.js'
        )

    def __init__(self, attrs=None):
        super(CustomOSMWidget, self).__init__()
        for key in ('default_lon', 'default_lat'):
            self.attrs[key] = getattr(self, key)
        if attrs:
            self.attrs.update(attrs)

    @property
    def map_srid(self):
        # Use the official spherical mercator projection SRID when GDAL is
        # available; otherwise, fallback to 900913.
        if gdal.HAS_GDAL:
            return 3857
        else:
            return 900913


class CampusForm(forms.ModelForm):
    location = forms.PointField(
        widget=
        CustomOSMWidget(
            attrs={'map_width': 1140, 'map_height': 500}
        ))
    courses = forms.ModelMultipleChoiceField(
        queryset=Course.objects.all(),
        label='Select course',
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name='course',
            is_stacked=False
        )
    )

    class Meta:
        model = Campus
        fields = ('campus', 'location', 'courses')

    def __init__(self, *args, **kwargs):
        try:
            self.user
        except AttributeError:
            self.user = kwargs.pop('user')

        if not self.user:
            raise Http404
        self.helper = FormHelper()
        form_title = 'Provider Admin'
        layout = Layout(
            Fieldset(
                form_title,
                Field('campus', css_class='form-control'),
                Field('location', css_class='form-control'),
                Field('courses', css_class='form-control'),
                css_id='form')
        )
        self.helper.layout = layout
        self.helper.html5_required = False
        self.helper.form_tag = False

        super(CampusForm, self).__init__(*args, **kwargs)
