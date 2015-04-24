# coding=utf-8
"""Model class for Education and Training Quality Assurance (ETQA)."""
__author__ = 'Christian Christelis <christian@kartoza.com>'
__date__ = '04/2015'
__license__ = "GPL"
__copyright__ = 'kartoza.com'

from django.contrib.gis.db import models


class FieldOfStudy(models.Model):
    id = models.AutoField(primary_key=True)
    field_of_study_class = models.IntegerField()
    field_of_study_description = models.CharField(
        max_length=50,
        blank=True,
        null=True)

    objects = models.GeoManager()

    def __unicode__(self):
        return 'Field of Study Class (%s)' % self.field_of_study_class

    class Meta:
        app_label = 'feti'