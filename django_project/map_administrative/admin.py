from django.contrib.gis import admin

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '19/09/16'
__license__ = "GPL"
__copyright__ = 'kartoza.com'

from .models.country import Country
from .models.province import Province

admin.site.register(Country, admin.ModelAdmin)
admin.site.register(Province, admin.ModelAdmin)
