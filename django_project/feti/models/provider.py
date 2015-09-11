# coding=utf-8
from django.contrib.gis.db import models
#from feti.models.address import Address

__author__ = 'Rizky Maulana Nugraha "lucernae" <lana.pcfre@gmail.com>'
__date__ = '16/04/15'


class Provider(models.Model):
    """Models to persist provider"""

    PROVIDER_STATUS_PRIVATE = False
    PROVIDER_STATUS_PUBLIC = True

    id = models.AutoField(primary_key=True)
    # provider_address = models.ForeignKey(Address)
    primary_institution = models.CharField(
        "Primary institution",
        max_length=255, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    status = models.BooleanField(default=PROVIDER_STATUS_PUBLIC)
    """public owned or private owned"""
    objects = models.GeoManager()

    def __unicode__(self):
        return self.primary_institution.title() or 'N/A'

    class Meta:
        app_label = 'feti'
        ordering = ['primary_institution']
        verbose_name = "Primary institution"
