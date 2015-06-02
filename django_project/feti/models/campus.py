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
        courses_string = '</li><li>'.join(
            [
                (
                    c.education_training_quality_assurance.body_name.strip() +
                    ' : ' +
                    c.description or '' +
                    ' - ' +
                    c.field_of_study.field_of_study_description or '')
                for c in self.courses.all()])

        result = (u'<p>{} : {}</p>'
                  u'<p>{}</p>'
                  u'<p>Courses : '
                  u'<br/>'
                  u'<ul><li>{}</li></ul>'
                  u'</p>').format(
            self.campus_name or '',
            self.provider.primary_institution or '',
            self.address.__unicode__() or '',
            courses_string or '')
        return result

    @property
    def geom(self):
        return self.location

    @property
    def campus_name(self):
        if self.campus:
            return self.campus
        else:
            return 'Unknown campus'

    def __unicode__(self):
        return u'%s' % self.campus_name