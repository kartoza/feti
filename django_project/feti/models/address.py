# coding=utf-8
from django.contrib.gis.db import models

__author__ = 'Rizky Maulana Nugraha "lucernae" <lana.pcfre@gmail.com>'
__date__ = '16/04/15'


class Address(models.Model):
    """Models to persist address information of providers and campus"""
    id = models.AutoField(primary_key=True)
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100)
    address3 = models.CharField(max_length=100)
    town = models.CharField(max_length=100)
    postal_code = models.IntegerField(max_length=4)
    phone = models.CharField(max_length=12)

    class Meta:
        app_label = 'feti'