from django.contrib import admin
from user_profile.models import CampusOfficial, ProviderOfficial


class CampusOfficialAdmin(admin.ModelAdmin):
    """Admin Class for Courses Model."""
    list_display = ('user',)
    filter_horizontal = ['campus']


admin.site.register(CampusOfficial, CampusOfficialAdmin)


class ProviderOfficialAdmin(admin.ModelAdmin):
    """Admin Class for Courses Model."""
    list_display = ('user',)
    filter_horizontal = ['provider']


admin.site.register(ProviderOfficial, ProviderOfficialAdmin)
