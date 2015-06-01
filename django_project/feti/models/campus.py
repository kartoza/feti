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
    campus = models.CharField(max_length=150, blank=True, null=True)
    location = models.PointField(blank=True, null=True)
    address = models.ForeignKey(Address)
    provider = models.ForeignKey(Provider)
    courses = models.ManyToManyField(Course)

    objects = models.GeoManager()

    class Meta:
        app_label = 'feti'

    @property
    def popup_content(self):
        courses_string = '</li><li>'.join([c.course_description for c in
                                           self.courses.all()])

        return ('<p>{} : {}</p>'
                '<p>{}</p>'
                '<p>Courses : '
                '<br/>'
                '<ul><li>{}</li></ul>'
                '</p>').format(
            self.campus,
            self.provider.primary_institution,
            self.address,
            courses_string)

    @property
    def geom(self):
        return self.location

    def __unicode__(self):
        return u'%s' % self.campus