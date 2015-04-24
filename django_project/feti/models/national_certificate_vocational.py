# coding=utf-8
"""Model class for WMS Resource"""
__author__ = 'Christian Christelis <christian@kartoza.com>'
__date__ = '04/2015'
__license__ = "GPL"
__copyright__ = 'kartoza.com'

from django.contrib.gis.db import models


class NationalCertificateVocational(models.Model):
    id = models.AutoField(primary_key=True)
    national_certificate_vocational_level = models.IntegerField()
    national_certificate_vocational_description = models.CharField(
        max_length=255,
        blank=True,
        null=True)

    objects = models.GeoManager()

    def __unicode__(self):
        return 'National Certificate Vocational Level (%s)' % (
            self.national_certificate_vocational_level)

    class Meta:
        app_label = 'feti'