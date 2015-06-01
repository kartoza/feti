# coding=utf-8
"""Model class for Education and Training Quality Assurance (ETQA)."""
__author__ = 'Christian Christelis <christian@kartoza.com>'
__date__ = '04/2015'
__license__ = "GPL"
__copyright__ = 'kartoza.com'

from django.contrib.gis.db import models
from django.core.validators import RegexValidator


class Address(models.Model):
    """The campus' address of the campus."""
    address_line_1 = models.CharField(max_length=100, blank=True, null=True)
    address_line_2 = models.CharField(max_length=100, blank=True, null=True)
    address_line_3 = models.CharField(max_length=100, blank=True, null=True)
    town = models.CharField(max_length=100, blank=True, null=True)

    postal_code_regex = RegexValidator(
        regex=r'^\d{4,4}$',
        message="Postal code consists of 4 digits.")
    postal_code = models.CharField(
        max_length=4,
        blank=True, null=True,
        validators=[postal_code_regex])

    phone_regex = RegexValidator(
        regex=r'^\+\d{12,12}$',
        message="Phone number should have the following format: "
                "'+27888888888'.")
    phone = models.CharField(
        max_length=100,
        validators=[phone_regex],
        blank=True,
        null=True)

    objects = models.GeoManager()

    def __unicode__(self):
        return '%s\n%s\n%s\n%s' % (
            self.address_line_1,
            self.address_line_2,
            self.address_line_3,
            self.postal_code)

    class Meta:
        app_label = 'feti'
