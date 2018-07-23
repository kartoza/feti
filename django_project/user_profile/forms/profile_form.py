from django.contrib.gis import forms
from django.contrib.auth.models import User
from betterforms.multiform import MultiModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout,
    Fieldset,
    Field,
)
from user_profile.models.profile import Profile
from core.widgets.custom_osm_widget import CustomOSMWidget


class UserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        form_title = 'Profile'
        layout = Layout(
            Fieldset(
                form_title,
                Field('first_name', css_class='form-control'),
                Field('last_name', css_class='form-control'),
                Field('email', css_class='form-control'),
            )
        )
        self.helper.layout = layout
        self.helper.html5_required = False
        self.helper.form_tag = False
        super(UserForm, self).__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileForm(forms.ModelForm):
    birth_date = forms.DateField(
        widget=forms.TextInput(
            attrs={'type': 'date'}
        ),
        required=False
    )

    location = forms.PointField(
        widget=
        CustomOSMWidget(
            attrs={'map_width': 1140, 'map_height': 500}
        ),
        required=False
    )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        layout = Layout(
            Fieldset(
                Field('bio', css_class='form-control'),
                Field('location', css_class='form-control'),
                Field('birth_date', css_class='form-control'),
                Field('picture', css_class='form-control'),
            )
        )
        self.helper.layout = layout
        self.helper.html5_required = False
        self.helper.form_tag = False
        super(ProfileForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Profile
        fields = ('bio', 'location', 'birth_date', 'picture')


class UserEditMultiForm(MultiModelForm):
    form_classes = {
        'user': UserForm,
        'profile': ProfileForm,
    }
