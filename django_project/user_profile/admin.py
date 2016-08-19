from django.contrib import admin
from user_profile.models import CampusOfficial


class CampusOfficialAdmin(admin.ModelAdmin):
    """Admin Class for Courses Model."""
    list_display = ('user', 'department', 'campus')


admin.site.register(CampusOfficial, CampusOfficialAdmin)
