# coding=utf-8
from django.contrib.gis.db import models
from feti.models.campus import Campus
from feti.models.course import Course

__author__ = 'Rizky Maulana Nugraha "lucernae" <lana.pcfre@gmail.com>'
__date__ = '24/07/15'


class CampusCourseEntry(models.Model):
    """
    Integrated model of relationships between Campus and Course.

    Mainly used for indexing purposes
    """

    id = models.AutoField(primary_key=True)
    campus = models.ForeignKey(Campus)
    course = models.ForeignKey(Course)

    class Meta:
        app_label = 'feti'
        managed = True
