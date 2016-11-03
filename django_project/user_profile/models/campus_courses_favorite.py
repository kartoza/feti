# coding=utf-8
from django.contrib.gis.db import models
from django.contrib.auth.models import User
from feti.models.campus import Campus
from feti.models.course import Course

__author__ = 'Dimas Ciputra <dimas@kartoza.com>'
__date__ = '01/11/16'


class CampusCoursesFavorite(models.Model):
    """
    Integrated model of relationships between Campus, Courses and user.
    """
    user = models.ForeignKey(User)
    campus = models.ForeignKey(Campus)
    courses = models.ManyToManyField(Course)

    class Meta:
        app_label = 'feti'
