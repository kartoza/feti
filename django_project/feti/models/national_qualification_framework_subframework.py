from django.contrib.gis.db import models


class NationalQualificationFrameworkSubFramework(models.Model):
    """
    Model for National Qualification
    Framework Sub-Framework (NQFSF).
    """
    code = models.CharField(
        max_length=50,
        blank=False,
        null=False
    )

    title = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )

    objects = models.GeoManager()

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return '%s - %s' % (self.code, self.title)

    class Meta:
        app_label = 'feti'
