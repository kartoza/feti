import datetime
from django.contrib.gis.db import models
from django.utils.crypto import get_random_string
from django.utils.translation import ugettext_lazy as _

__author__ = 'Dimas Ciputra <dimas@kartoza.com>'
__date__ = '20/09/16'


def random_string():
    while True:
        try:
            random_string = get_random_string()
            URL.objects.get(random_string=random_string)
        except URL.DoesNotExist:
            return random_string


class URL(models.Model):
    """Models to URL"""

    id = models.AutoField(primary_key=True)

    random_string = models.CharField(
        _("Random Words"),
        max_length=255,
        blank=False,
        null=False,
        unique=True,
        default=random_string)
    url = models.URLField(
        _("Url"),
        max_length=1000,
        blank=False,
        null=False)
    date = models.DateField(_("Date"), default=datetime.date.today)

    def __unicode__(self):
        return self.random_words

    class Meta:
        app_label = 'feti'
        ordering = ['date']
        verbose_name = "URL"
