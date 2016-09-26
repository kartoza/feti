# coding=utf-8
"""Model class for WMS Resource"""
__author__ = 'Christian Christelis <christian@kartoza.com>'
__project_name = 'watchkeeper'
__filename = 'boundary.py'
__date__ = '19/06/2015'

from django.contrib.gis.db import models


class Boundary(models.Model):
    """This is an abstract model that vectors can inherit from. e.g. country"""
    name = models.CharField(
        verbose_name='',
        help_text='',
        max_length=50,
        null=False,
        blank=False)

    polygon_geometry = models.MultiPolygonField(
        srid=4326)

    id = models.AutoField(
        primary_key=True)

    objects = models.GeoManager()

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return self.name

    class Meta:
        abstract = True
        app_label = 'map_administrative'
