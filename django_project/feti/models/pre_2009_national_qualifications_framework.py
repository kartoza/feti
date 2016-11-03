from django.contrib.gis.db import models


class Pre2009NationalQualificationsFramework(models.Model):

    level = models.CharField(
        max_length=150,
        blank=False,
        null=False
    )

    objects = models.GeoManager()

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return self.level

    class Meta:
        app_label = 'feti'
