# coding=utf-8
"""Model class for Education and Training Quality Assurance (ETQA)."""

from django.contrib.gis.db import models

from feti.models.campus import Campus
from feti.models.course import Course

__author__ = 'Christian Christelis <christian@kartoza.com>'
__date__ = '04/2015'
__license__ = "GPL"
__copyright__ = 'kartoza.com'


class CourseProviderLink(models.Model):
    """
    Integrated model of relationships between course and campus.

    Used for indexing purposes.
    """
    id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course)
    campus = models.ForeignKey(Campus)

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return '%s at %s' % (
            self.course.__unicode__(),
            self.campus.__unicode__())

    objects = models.GeoManager()

    class Meta:
        app_label = 'feti'
