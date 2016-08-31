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

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '09/08/16'
__license__ = "GPL"
__copyright__ = 'kartoza.com'


class CampusForm(forms.ModelForm):
    location = forms.PointField(
        widget=
        forms.OSMWidget(attrs={'map_width': 1140, 'map_height': 500}))
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
                css_id='project-form')
        )
        self.helper.layout = layout
        self.helper.html5_required = False

        super(CampusForm, self).__init__(*args, **kwargs)

        # init choice
        self.helper.add_input(Submit('submit', 'Submit'))

    class Media:
        css = {'all': ['admin/css/widgets.css', '/static/grappelli/jquery/ui/jquery-ui.min.css',
                       '/static/grappelli/stylesheets/screen.css']}
        js = ['/custom_admin/jsi18n',
              '/static/grappelli/jquery/jquery-2.1.4.min.js',
              "/static/grappelli/jquery/ui/jquery-ui.min.js",
              "/static/grappelli/js/grappelli.min.js",
              '/static/feti/js/libs/grappelli_override.js',
              '/static/admin/js/SelectBox.js',
              '/static/admin/js/SelectFilter2.js']
