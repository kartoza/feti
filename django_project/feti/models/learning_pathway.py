__author__ = 'Christian Christelis <christian@kartoza.com>'
__date__ = '07/09/16'

from django.contrib.gis.db import models

from feti.models.course import Course

class Step(models.Model):
    """The step that needs to be taken on this learning pathway"""
    step_number = models.IntegerField()
    title = models.CharField(max_length=255, null=True, blank=True)
    detail = models.CharField(max_length=510, null=True, blank=True)
    course = models.ForeignKey(Course, null=True, blank=True)

    class Meta:
        app_label = 'feti'
        managed = True


class LearningPathway(models.Model):
    """A Learning Pathway where a set of courses are offered."""
    id = models.AutoField(primary_key=True)
    pathway_number = models.IntegerField()
    steps = models.ManyToManyField(Step)  ## Limit choices to or exclude already selected step numbers in admin

    class Meta:
        app_label = 'feti'
        managed = True
