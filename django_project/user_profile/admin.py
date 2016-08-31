from django.contrib import admin
from user_profile.models import CampusOfficial


class CampusOfficialAdmin(admin.ModelAdmin):
    """Admin Class for Courses Model."""
    list_display = ('user', 'department')
    filter_horizontal = ['campus']


admin.site.register(CampusOfficial, CampusOfficialAdmin)
