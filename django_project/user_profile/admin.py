from django.contrib import admin
from user_profile.models import CampusOfficial, ProviderOfficial
from user_profile.models.profile import Profile


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


admin.site.register(ProviderOfficial, ProviderOfficialAdmin)
admin.site.register(Profile, ProfileAdmin)
