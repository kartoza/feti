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
        regex=r'^\+?(\d)+(\d(-)?)*(\d)+$',
        message="Phone number should have the following format: "
                "'+27888888888 or 021-777-777'.")
    phone = models.CharField(
        max_length=100,
        validators=[phone_regex],
        blank=True,
        null=True)

    # Foreign key link to campus
    # needed for inline admin interface
    campus_fk = models.OneToOneField(
        'Campus', related_name='address_fk', null=True)

    objects = models.GeoManager()

    def __unicode__(self):
        address_list = [
            self.address_line_1,
            self.address_line_2,
            self.address_line_3,
            self.town,
            u'Postal Code: ' + unicode(self.postal_code) if self.postal_code
            else u'',
            u'Phone: ' + unicode(self.phone) if self.phone else u''
        ]
        concat_list = [l for l in address_list if l and l.strip()]
        address_string = u', \n'.join(concat_list)
        if not address_string.strip():
            address_string = 'N/A'
        return address_string

    @property
    def address_line(self):
        address_list = [
            self.address_line_1,
            self.address_line_2,
            self.address_line_3
        ]
        concat_list = [l for l in address_list if l and l.strip()]
        address_string = u', \n'.join(concat_list)
        if not address_string.strip():
            address_string = 'N/A'
        return address_string

    class Meta:
        app_label = 'feti'
        verbose_name_plural = 'Addreses'
