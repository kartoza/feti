# coding=utf-8
"""Model class for District"""
from django.contrib.gis.db import models

from .boundary import Boundary
from .district import District


class Municipality(Boundary):
    """Class for Municipality."""

    district = models.ForeignKey(District)

    class Meta:
        """Meta Class"""
        app_label = 'map_administrative'
        verbose_name_plural = 'Municipalities'
        ordering = ['name']

    def parent(self):
        return '%s,%s' % (self.district.parent(), self.district.name)


Municipality._meta.get_field('name').verbose_name = 'Municipality'
Municipality._meta.get_field('name').help_text = (
    'The name of municipality.')
