# coding=utf-8
from django.contrib.gis.db import models
from feti.models.field_of_study import FieldOfStudy
from feti.models.subfield_of_study import SubFieldOfStudy


class FieldSubfieldOfStudy(models.Model):
    """
    Integrated model of relationships between Subfield and Field of study.
    """

    id = models.AutoField(primary_key=True)
    field_of_study = models.ForeignKey(FieldOfStudy)
    subfield_of_study = models.ManyToManyField(SubFieldOfStudy)

    class Meta:
        app_label = 'feti'
        managed = True

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return 'Field %s' % self.field_of_study.field_of_study_description
