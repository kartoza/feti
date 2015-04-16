# coding=utf-8
"""Model class for Education and Training Quality Assurance (ETQA)."""
__author__ = 'Christian Christelis <christian@kartoza.com>'
__date__ = '04/2015'
__license__ = "GPL"
__copyright__ = 'kartoza.com'

from django.contrib.gis.db import models

class EducationTrainingQualityAssurance(models.Model):
    acronym = models.CharField(max_length=30)
    body_name = models.CharField(max_length=255)
    url = models.URLField()

    def __unicode__(self):
        return '%s (%s)' % (self.acronym, self.acronym)

    class Meta:
        app_label = 'feti'
