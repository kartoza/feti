# coding=utf-8
"""Model class for WMS Resource"""

__author__ = 'Christian Christelis <christian@kartoza.com>'
__date__ = '04/2015'
__license__ = "GPL"
__copyright__ = 'kartoza.com'

from django.contrib.gis.db import models

from feti.models.provider import Provider
from feti.models.address import Address
from feti.models.course import Course


class Campus(models.Model):
    """A campus where a set of courses are offered."""
    id = models.AutoField(primary_key=True)
    campus = models.CharField(max_length=100, blank=True, null=True)
    location = models.PointField()
    address = models.ForeignKey(Address)
    provider = models.ForeignKey(Provider)
    courses = models.ManyToManyField(Course)

    objects = models.GeoManager()

    class Meta:
        app_label = 'feti'

    @property
    def popup_content(self):
        courses_string = '</li><li>'.join([c.course_description for c
                                           in self.courses.all()])

        result = (u'<p>{} : {}</p>'
                  u'<p>{}</p>'
                  u'<p>Courses : '
                  u'<br/>'
                  u'<ul><li>{}</li></ul>'
                  u'</p>').format(
            self.campus,
            self.provider,
            self.address,
            courses_string)
        return result

    @property
    def geom(self):
        return self.location

    def __unicode__(self):
        return u'%s' % self.campus