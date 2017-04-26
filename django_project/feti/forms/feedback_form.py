# coding=utf-8

from django.contrib import messages
from django.contrib.gis import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout,
    Fieldset,
    Submit,
    Field,
)
from feti.models.feedback import Feedback

__author__ = 'Anita Hapsari <anita@kartoza.com>'
__date__ = '25/04/17'


class FeedbackForm(forms.ModelForm):

    class Meta:
        model = Feedback
        fields = (
            'title',
            'name',
            'contact',
            'comments',
        )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        form_title = 'Feedback Form'
        layout = Layout(
            Fieldset(
                form_title,
                Field('title', css_class='form-control'),
                Field('name', css_class='form-control'),
                Field('contact', css_class='form-control'),
                Field('comments', css_class='form-control'))
        )
        self.helper.layout = layout
        self.helper.html5_required = False
        super(FeedbackForm, self).__init__(*args, **kwargs)
        self.helper.add_input(Submit('submit', 'Submit'))

    def save(self, commit=True):
        super(FeedbackForm, self).save(commit=True)
