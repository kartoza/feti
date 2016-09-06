from django.contrib.auth.models import User
from django.db import models
from feti.models.campus import Campus


class CampusOfficial(models.Model):
    # official user that have provider
    user = models.OneToOneField(User)
    campus = models.ManyToManyField(Campus, verbose_name="Providers")

    class Meta:
        app_label = "feti"
        verbose_name = 'Provider Official'

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return self.user.username
