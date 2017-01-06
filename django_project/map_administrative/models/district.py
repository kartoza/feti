# coding=utf-8
"""Model class for District"""
from django.contrib.gis.db import models

from .boundary import Boundary
from .province import Province


class District(Boundary):
    """Class for District."""

    province = models.ForeignKey(Province)

    class Meta:
        """Meta Class"""
        app_label = 'map_administrative'
        verbose_name_plural = 'Districts'
        ordering = ['name']

    def parent(self):
        return self.province.name


District._meta.get_field('name').verbose_name = 'District'
District._meta.get_field('name').help_text = (
    'The name of district.')
