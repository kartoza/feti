# coding=utf-8
from django.contrib.gis.db import models

__author__ = 'Rizky Maulana Nugraha "lucernae" <lana.pcfre@gmail.com>'
__date__ = '23/04/15'


class NationalQualificationsFramework(models.Model):
    """Model for National Qualifications Framework (NQF)"""
    level = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=50)
    certification = models.CharField(max_length=4)
    link = models.URLField()

    class Meta:
        app_label = 'feti'
