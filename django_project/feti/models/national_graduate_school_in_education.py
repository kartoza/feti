# coding=utf-8
from django.contrib.gis.db import models

__author__ = 'Rizky Maulana Nugraha "lucernae" <lana.pcfre@gmail.com>'
__date__ = '23/04/15'


class NationalGraduateSchoolInEducation(models.Model):
    """Model for National Graduate School in Education (NATED)"""
    id = models.AutoField(primary_key=True)
    level = models.CharField(max_length=2)
    description = models.CharField(max_length=100)

    objects = models.GeoManager()

    def __unicode__(self):
        return 'National Graduate School in Education Level (%s)' % self.level

    class Meta:
        app_label = 'feti'
