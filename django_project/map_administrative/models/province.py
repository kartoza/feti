# coding=utf-8
"""Model class for the concrete Province (or State.)"""
__author__ = 'Christian Christelis <christian@kartoza.com>'
__project_name = 'watchkeeper'
__filename = 'province.py'
__date__ = '19/06/2015'

from django.contrib.gis.db import models

from .boundary import Boundary
from .country import Country


class Province(Boundary):
    """Class for Country."""

    country = models.ForeignKey(Country)

    class Meta:
        """Meta Class"""
        app_label = 'map_administrative'
        verbose_name_plural = 'Provinces'
        ordering = ['name']

    def parent(self):
        return self.country.name


Province._meta.get_field('name').verbose_name = 'Province or State name'
Province._meta.get_field('name').help_text = (
    'The name of the province or state.')
