# coding=utf-8
"""Model class for feedback"""

from django.db import models
from django.utils import timezone


class Feedback(models.Model):
    """Input feedback."""

    title = models.CharField(
        max_length=250,
        null=False,
        blank=False
    )

    name = models.CharField(
        max_length=200,
        null=False,
        blank=False
    )

    contact = models.CharField(
        max_length=200,
        null=False,
        blank=False
    )

    comments = models.TextField(
        max_length=500,
        null=False,
        blank=False
    )

    read = models.BooleanField(
        help_text='Feedback is read/processed',
        default=False
    )

    date = timezone.now()

    class Meta:
        ordering = ['title']

    def save(self, *args, **kwargs):
        super(self, Feedback).save(*args, **kwargs)

    def __unicode__(self):
        return '%s' % self.title
