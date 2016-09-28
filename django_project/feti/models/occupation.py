__author__ = 'Christian Christelis <christian@kartoza.com>'
__date__ = '06/09/16'
__license__ = "GPL"
__copyright__ = 'kartoza.com'

# coding=utf-8
"""Model class for Occupations"""

from django.contrib.gis.db import models
from django.core import management
from django.db.models.signals import post_save


class Occupation(models.Model):
    """A campus where a set of courses are offered."""
    id = models.AutoField(primary_key=True)
    occupation = models.CharField(max_length=150, blank=False, null=False, unique=True)
    green_occupation = models.BooleanField(default=False)
    scarce_skill = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)
    tasks = models.TextField(blank=True, null=True)
    occupation_regulation = models.TextField(blank=True, null=True)
    learning_pathway_description = models.TextField(blank=True, null=True)

    class Meta:
        app_label = 'feti'
        managed = True

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return u'%s' % self.occupation

def generate_occupation_index(sender, instance, **kwargs):
    management.call_command('generate_occupation_index')
