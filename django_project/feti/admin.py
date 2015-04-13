# coding=utf-8
"""Model Admin Class."""

from django.contrib import admin
from feti.models.campus import Campus


class CampusAdmin(admin.ModelAdmin):
    """Admin Class for FloodReport Model."""
    list_display = ('campus',)
    list_filter = ['campus', ]
    search_fields = ['campus', ]

admin.site.register(Campus, CampusAdmin)
