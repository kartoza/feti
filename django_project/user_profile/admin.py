from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from user_profile.models import Official


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class OfficialInline(admin.StackedInline):
    model = Official
    can_delete = False
    verbose_name_plural = 'officials'


# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (OfficialInline, )

# Re-register UserAdmin
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)
