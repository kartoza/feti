from django.contrib.gis import admin

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '19/09/16'
__license__ = "GPL"
__copyright__ = 'kartoza.com'

from .models.country import Country
from .models.province import Province
from .models.district import District
from .models.municipality import Municipality

admin.site.register(Country, admin.ModelAdmin)
admin.site.register(Province, admin.ModelAdmin)
admin.site.register(District, admin.ModelAdmin)
admin.site.register(Municipality, admin.ModelAdmin)
