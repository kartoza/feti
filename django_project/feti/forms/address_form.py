from django.contrib.gis import forms
from feti.models.address import Address
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


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('address_line_1', 'address_line_2', 'address_line_3', 'town',
                  'postal_code', 'phone')

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        form_title = 'Address Admin'
        layout = Layout(
            Fieldset(
                form_title,
                Field('address_line_1', css_class='form-control'),
                Field('address_line_2', css_class='form-control'),
                Field('address_line_3', css_class='form-control'),
                Field('town', css_class='form-control'),
                Field('postal_code', css_class='form-control'),
                Field('phone', css_class='form-control'))
        )
        self.helper.layout = layout
        self.helper.html5_required = False
        self.helper.form_tag = False

        super(AddressForm, self).__init__(*args, **kwargs)
