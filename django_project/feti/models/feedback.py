# coding=utf-8
"""Model class for feedback"""

import datetime
from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _

__author__ = 'Anita Hapsari <anita@kartoza.com>'
__date__ = '25/04/17'


class Feedback(models.Model):
    """Input feedback."""

    title = models.CharField(
        _("Title"),
        max_length=250,
        null=False,
        blank=False
    )

    name = models.CharField(
        _("Name"),
        max_length=200,
        null=False,
        blank=False
    )

    contact = models.CharField(
        _("Contact"),
        max_length=200,
        null=False,
        blank=False
    )

    comments = models.TextField(
        _("Comments"),
        max_length=500,
        null=False,
        blank=False
    )

    read = models.BooleanField(
        _("Read"),
        help_text='Feedback is read/processed',
        default=False
    )

    date = models.DateField(_("Date"), default=datetime.date.today)

    class Meta:
        app_label = 'feti'
        ordering = ['title']

    def save(self, *args, **kwargs):
        super(Feedback, self).save(*args, **kwargs)

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return u'%s' % self.title
