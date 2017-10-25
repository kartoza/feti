# coding=utf-8
"""Model class for WMS Resource"""

from django.contrib.gis.db import models

__author__ = 'Christian Christelis <christian@kartoza.com>'
__date__ = '04/2015'
__license__ = "GPL"
__copyright__ = 'kartoza.com'


class NationalCertificateVocational(models.Model):
    """
    The level description for a
    national certificate vocational.
    """
    id = models.AutoField(primary_key=True)
    national_certificate_vocational_level = models.IntegerField()
    national_certificate_vocational_description = models.CharField(
        max_length=255,
        blank=True,
        null=True)

    objects = models.GeoManager()

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return 'National Certificate Vocational Level (%s)' % (
            self.national_certificate_vocational_level)

    class Meta:
        app_label = 'feti'
