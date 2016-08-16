from django import forms
from django.http import Http404
from feti.models.campus import Campus
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


class CampusForm(forms.ModelForm):
    class Meta:
        model = Campus
        fields = ('campus', 'courses')

    def __init__(self, *args, **kwargs):
        try:
            self.user
        except AttributeError:
            self.user = kwargs.pop('user')

        if not self.user:
            raise Http404
        self.helper = FormHelper()
        form_title = 'Campus Course Admin'
        layout = Layout(
            Fieldset(
                form_title,
                Field('campus', css_class='form-control'),
                Field('courses', css_class='form-control'),
                css_id='project-form')
        )
        self.helper.layout = layout
        self.helper.html5_required = False

        super(CampusForm, self).__init__(*args, **kwargs)

        # init choice
        self.helper.add_input(Submit('submit', 'Submit'))
