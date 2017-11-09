from django.contrib.gis.db import models


class QualClass(models.Model):
    """Model to define a Qualification class."""
    title = models.CharField(
        max_length=150,
        blank=False,
        null=False)

    objects = models.GeoManager()

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return self.title

    class Meta:
        app_label = 'feti'
