from django.contrib.gis.db import models


class QualificationType(models.Model):
    """Model for a type of qualification."""
    type = models.CharField(
        max_length=150,
        blank=False,
        null=False)

    objects = models.GeoManager()

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return self.type

    class Meta:
        app_label = 'feti'
