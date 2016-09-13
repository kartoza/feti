from django.contrib.auth.models import User
from django.db import models
from feti.models.provider import Provider


class ProviderOfficial(models.Model):
    # official user that have provider
    user = models.OneToOneField(User)
    provider = models.ManyToManyField(Provider, verbose_name="Primary Institution")

    class Meta:
        app_label = "feti"
        verbose_name = 'Primary Institution Official'

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return self.user.username
