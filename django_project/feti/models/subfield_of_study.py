"""Model class for Subfield of course"""

from django.contrib.gis.db import models


class SubFieldOfStudy(models.Model):
    """Model for a sub-field of study."""
    learning_subfield = models.CharField(
        max_length=150,
        blank=False,
        null=False)

    objects = models.GeoManager()

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return self.learning_subfield

    class Meta:
        app_label = 'feti'
