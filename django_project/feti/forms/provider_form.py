from django.contrib.gis import forms
from django.http import Http404
from feti.models.provider import Provider
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout,
    Fieldset,
    Submit,
    Field,
)

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '09/08/16'
__license__ = "GPL"
__copyright__ = 'kartoza.com'


class ProviderForm(forms.ModelForm):
    class Meta:
        model = Provider
        fields = ('primary_institution', 'website', 'status')

    def __init__(self, *args, **kwargs):
        try:
            self.user
        except AttributeError:
            self.user = kwargs.pop('user')

        if not self.user:
            raise Http404
        self.helper = FormHelper()
        form_title = 'Primary Institute Admin'
        layout = Layout(
            Fieldset(
                form_title,
                Field('primary_institution', css_class='form-control'),
                Field('website', css_class='form-control'),
                Field('status', css_class='form-control'),
                css_id='project-form')
        )
        self.helper.layout = layout
        self.helper.html5_required = False

        super(ProviderForm, self).__init__(*args, **kwargs)

        # init choice
        self.helper.add_input(Submit('submit', 'Submit'))
