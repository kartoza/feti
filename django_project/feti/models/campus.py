# coding=utf-8
"""Model class for WMS Resource"""
__author__ = 'Christian Christelis <christian@kartoza.com>'
__date__ = '04/2015'
__license__ = "GPL"
__copyright__ = 'kartoza.com'

from django.contrib.gis.db import models


class Campus(models.Model):
    id = models.AutoField(primary_key=True)
    """A campus where a set of courses are offered."""
    campus = models.CharField(max_length=100, blank=True, null=True)
    location = models.PointField()

    objects = models.GeoManager()

    class Meta:
        app_label = 'feti'
