# coding=utf-8
"""Model class for Education and Training Quality Assurance (ETQA)."""

from django.contrib.gis.db import models

__author__ = 'Christian Christelis <christian@kartoza.com>'
__date__ = '04/2015'
__license__ = "GPL"
__copyright__ = 'kartoza.com'


class FieldOfStudy(models.Model):
    id = models.AutoField(primary_key=True)
    field_of_study_class = models.IntegerField()
    field_of_study_description = models.CharField(
        max_length=150,
        blank=True,
        null=True)

    objects = models.GeoManager()

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return 'Field %s - %s' % (self.field_of_study_class, self.field_of_study_description)

    class Meta:
        app_label = 'feti'
