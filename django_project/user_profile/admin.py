from django.contrib import admin
from user_profile.models import CampusOfficial, ProviderOfficial, CampusCoursesFavorite
from user_profile.models.profile import Profile
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from django import forms

class CampusOfficialAdmin(admin.ModelAdmin):
    """Admin Class for Courses Model."""
    list_display = ('user',)
    filter_horizontal = ['campus']


admin.site.register(CampusOfficial, CampusOfficialAdmin)


class ProviderOfficialAdmin(admin.ModelAdmin):
    """Admin Class for Courses Model."""
    list_display = ('user',)
    filter_horizontal = ['provider']


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'birth_date')
    search_fields = ['user__username', 'birth_date']

    class Media:
        css = {
            'all': ('feti/css/feti-admin.css',)
        }


class CustomUserCreationForm(UserCreationForm):
    username = forms.RegexField(
        label='Username',
        max_length=30,
        regex=r'^[\w.]+$',
        help_text='Required. 30 characters or fewer. Alphanumeric characters only '
                  '(letters, digits and underscores).',
        error_message='This value must contain only letters, numbers and underscores.')


class CustomUserChangeForm(UserChangeForm):
    username = forms.RegexField(
        label='Username',
        max_length=30,
        regex=r'^[\w.]+$',
        help_text='Required. 30 characters or fewer. Alphanumeric characters only '
                  '(letters, digits and underscores).',
        error_message='This value must contain only letters, numbers and underscores.')


class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm


admin.site.register(ProviderOfficial, ProviderOfficialAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(CampusCoursesFavorite)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
