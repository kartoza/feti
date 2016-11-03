__author__ = 'Christian Christelis <christian@kartoza.com>'
__date__ = '07/09/16'

from django.contrib.gis.db import models

from feti.models.course import Course
from feti.models.occupation import Occupation


class StepDetail(models.Model):
    """The step that needs to be taken on this learning pathway"""
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    detail = models.CharField(max_length=1024, null=True, blank=True)
    course = models.ManyToManyField(Course, blank=True)

    class Meta:
        app_label = 'feti'
        managed = True
        unique_together = ('title', 'detail',)
        verbose_name = "step"
        verbose_name_plural = "steps"

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return u'%s' % self.title


class LearningPathway(models.Model):
    """A Learning Pathway where a set of courses are offered."""
    id = models.AutoField(primary_key=True)
    pathway_number = models.IntegerField()
    occupation = models.ForeignKey(
        Occupation, default=None, on_delete=models.CASCADE)

    class Meta:
        app_label = 'feti'
        managed = True

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return u'#%d' % self.pathway_number


class Step(models.Model):
    """The step that needs to be taken on this learning pathway"""
    step_number = models.IntegerField()
    step_detail = models.ForeignKey(
        StepDetail, default=None)
    learning_pathway = models.ForeignKey(
        LearningPathway, default=None, on_delete=models.CASCADE)

    class Meta:
        app_label = 'feti'
        managed = True
