import datetime
from django.contrib.gis.db import models
from django.utils.translation import ugettext, ugettext_lazy as _

__author__ = 'Dimas Ciputra <dimas@kartoza.com>'
__date__ = '20/09/16'


class URL(models.Model):
    """Models to URL"""

    id = models.AutoField(primary_key=True)

    random_string = models.CharField(
        _("Random Words"),
        max_length=255,
        blank=False,
        null=False)
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
