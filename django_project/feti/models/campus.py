# coding=utf-8
"""Model class for WMS Resource"""

__author__ = 'Christian Christelis <christian@kartoza.com>'
__date__ = '04/2015'
__license__ = "GPL"
__copyright__ = 'kartoza.com'

from django.contrib.gis.db import models
from django.template import Context, loader

from feti.models.provider import Provider
from feti.models.course import Course


class Campus(models.Model):
    """A campus where a set of courses are offered."""
    id = models.AutoField(primary_key=True)
    campus = models.CharField(max_length=150, blank=True, null=True)
    location = models.PointField(blank=True, null=True)
    address = models.ForeignKey('Address')
    provider = models.ForeignKey(Provider)
    courses = models.ManyToManyField(Course)

    # Decreasing the number of links needed to other models for descriptions.
    _long_description = models.CharField(
        max_length=510,
        blank=True,
        null=True
    )
    # Decreasing the number of links needed to get popup material
    _campus_popup = models.CharField(
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
    def related_course(self):
        return self._related_course

    @related_course.setter
    def related_course(self, value):
        self._related_course = value

    @property
    def popup_content(self):
        related_course = self.related_course
        if not related_course:
            related_course = self.courses.all()
        courses_string = u''
        for c in related_course:
            courses_string += u'<li>' + c.course_popup + u'</li>'

        popup_format = (
            u'<div>{}</div>')

        if related_course:
            popup_format += (
                u'<p>Courses : '
                u'<div class="course-list"><ul>{}</ul></div>'
                u'</p>')

        result = popup_format.format(
            self.campus_popup or u'',
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
    def campus_popup(self):
        return self._campus_popup

    @property
    def incomplete(self):
        return not self._complete

    def __unicode__(self):
        return u'%s' % self.campus_name

    def save(self, *args, **kwargs):
        # set up long description
        self._long_description = u'%s - %s' % (
            self.provider.primary_institution.strip(),
            self.campus_name.strip()
        )
        if not self.courses.count() or not self.location or not self.campus:
            # Only mark campuses without courses as incomplete
            self._complete = False
        else:
            self._complete = True

        # set up campus popup
        template = loader.get_template('feti/campus_popup.html')
        provider_name = self.provider.primary_institution if self.provider \
            else ''
        campus_name = self.address.town if self.address else 'N/A'
        address_full = self.address.address_line if self.address else 'N/A'
        website = self.provider.website if self.provider else 'N/A'
        phone = self.address.phone if self.address else 'N/A'
        variable = {
            'provider': provider_name,
            'campus': campus_name,
            'address_full': address_full,
            'website': website,
            'phone': phone
        }
        self._campus_popup = template.render(Context(variable))

        # save the key in address
        self.address_fk = self.address
        self.address_fk.campus_fk = self
        self.address_fk.save()

        # save campus course link
        from feti.models.campus_course_entry import CampusCourseEntry
        entries = []
        for course in self.courses.all():
            try:
                link = CampusCourseEntry.objects.get(
                    campus=self, course=course)
            except CampusCourseEntry.DoesNotExist:
                link = CampusCourseEntry.objects.create(
                    campus=self, course=course)
                entries.append(CampusCourseEntry(campus=self, course=course))

        CampusCourseEntry.objects.bulk_create(entries)

        super(Campus, self).save(*args, **kwargs)
