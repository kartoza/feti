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

    # Decreasing the number of links needed to other models for descriptions.
    _long_description = models.CharField(
        max_length=510,
        blank=True,
        null=True
    )
    # Manage campuses that we think have too little
    # data to be considered complete
    _complete = models.BooleanField(
        default=True)

    objects = models.GeoManager()

    class Meta:
        app_label = 'feti'
        verbose_name_plural = 'Campuses'

    @property
    def popup_content(self, related_course=None):
        if not related_course:
            related_course = self.courses.all()
        courses_string = u''
        for c in related_course:
            desc = c.long_description or u''
            if c.field_of_study and \
                    c.field_of_study.field_of_study_description:
                desc += u' - '
                desc += c.field_of_study.field_of_study_description
            courses_string += u'<li>' + desc + u'</li>'

        address = self.address.__unicode__() or u'' if self.address else u''

        popup_format =(
            u'<p>{}</p>'
            u'<p>{}</p>')

        if related_course:
            popup_format += (
                u'<p>Courses : '
                u'<br/>'
                u'<ul><li>{}</li></ul>'
                u'</p>')

        result = popup_format.format(
            self.long_description or u'',
            address,
            courses_string or u'')
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

    @property
    def long_description(self):
        return self._long_description

    @property
    def incomplete(self):
        return not self._complete

    def __unicode__(self):
        return u'%s' % self.campus_name

    def save(self, *args, **kwargs):
        self._long_description = '%s - %s' % (
            self.provider.primary_institution.strip(),
            self.campus_name.strip()
        )
        if not self.courses.count() or not self.location or not self.campus:
            # Only mark campuses without courses as incomplete
            self._complete = False
        else:
            self._complete = True
        super(Campus, self).save(*args, **kwargs)