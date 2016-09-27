# coding=utf-8
"""Model class for WMS Resource"""

from django.contrib.gis.db import models
from django.core import management
from django.db.models.signals import post_save
from django.template import Context, loader

from feti.models.provider import Provider
from feti.models.course import Course
from feti.models.address import Address

__author__ = 'Christian Christelis <christian@kartoza.com>'
__date__ = '04/2015'
__license__ = "GPL"
__copyright__ = 'kartoza.com'


class Campus(models.Model):
    """A campus where a set of courses are offered."""
    id = models.AutoField(primary_key=True)
    campus = models.CharField('Provider', max_length=150, blank=True, null=True)
    # default to south africa capital coordinate
    location = models.PointField(blank=True, null=True,
                                 default='POINT(28.034088 -26.195246)')
    address = models.ForeignKey('Address', null=True, blank=True)
    provider = models.ForeignKey(
        Provider, related_name='campuses')
    courses = models.ManyToManyField(Course)

    # Decreasing the number of links needed to other models for descriptions.
    _long_description = models.CharField(
        max_length=510,
        blank=True,
        null=True
    )
    # Decreasing the number of links needed to get popup material
    _campus_popup = models.CharField(
        max_length=1020,
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
        ordering = ['campus']
        verbose_name = 'Provider'

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
            u'<div class="leaflet-popup-content">{}</div>')

        if related_course:
            popup_format += (
                u'<div class="leaflet-courses">'
                u'<p>Courses : </p>'
                u'<ul>'
                u'{}'
                u'</ul>'
                u'</div>')

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

    @property
    def primary_institution(self):
        return self.provider

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return u'%s - %s' % (self.provider.__unicode__(),self.campus_name)

    def save(self, *args, **kwargs):
        # set up long description
        from_inline = False
        instance = super(Campus, self).save(*args, **kwargs)

        try:
            self.address_fk
            self.address
        except Exception as e:  # noqa
            from_inline = True

        if from_inline:
            # create new address placeholder
            self.address_fk = Address.objects.create()
            self.address = self.address_fk

        if self.provider:
            self._long_description = u'%s - %s' % (
                self.provider.primary_institution.strip(),
                self.campus_name.strip()
            )

        if not self.courses.count() or not self.location:
            # Only mark campuses without courses as incomplete
            self._complete = False
        else:
            self._complete = True

        # set up campus popup
        template = loader.get_template('feti/campus_popup.html')
        provider_name = self.provider.primary_institution if self.provider \
            else ''
        campus_name = self.campus_name if self.campus_name else 'N/A'
        address_full = 'N/A'
        if self.address:
            if self.address.address_line:
                address_full = self.address.address_line
        website = 'N/A'
        if self.provider:
            if self.provider.website:
                website = self.provider.website
        phone = 'N/A'
        if self.address:
            if self.address.phone:
                phone = self.address.phone
        variable = {
            'provider': provider_name,
            'campus': campus_name,
            'address_full': address_full,
            'website': website,
            'phone': phone
        }
        self._campus_popup = template.render(Context(variable))

        # save the key in address
        try:
            self.address_fk = self.address
            self.address_fk.campus_fk = self
            self.address_fk.save()
        except self.address.DoesNotExist:
            pass

        # save campus course link
        from feti.models.campus_course_entry import CampusCourseEntry
        entries = []
        for course in self.courses.all():
            try:
                CampusCourseEntry.objects.get(campus=self, course=course)
            except CampusCourseEntry.DoesNotExist:
                entries.append(CampusCourseEntry(campus=self, course=course))
            except CampusCourseEntry.MultipleObjectsReturned:
                redundant = CampusCourseEntry.objects.filter(
                    campus=self, course=course)[1:]
                for campus_course_entries in redundant:
                    campus_course_entries.delete()

        CampusCourseEntry.objects.bulk_create(entries)
        # delete entry not in course
        campus_course_entries = CampusCourseEntry.objects.filter(campus=self)
        course_ids = [c.id for c in self.courses.all()]
        for entry in campus_course_entries:
            if entry.course.id not in course_ids:
                entry.delete()

        return instance

    def delete(self, *args, **kwargs):
        # delete campus course entries
        from feti.models.campus_course_entry import CampusCourseEntry
        CampusCourseEntry.objects.filter(campus=self).delete()
        super(Campus, self).delete(*args, **kwargs)


def generate_campus_index(sender, instance, **kwargs):
    management.call_command('generate_campus_index')


post_save.connect(generate_campus_index, sender=Campus, dispatch_uid="generate_campus_index")
