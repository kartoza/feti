from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from feti.models.campus import Campus


class CampusOfficial(models.Model):
    # official user that have provider
    user = models.OneToOneField(User)
    department = models.CharField(max_length=100)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: "
                "'+6288888888888'. Up to 15 digits allowed.")
    phone = models.CharField(
        validators=[phone_regex], blank=True, max_length=15
    )
    campus = models.OneToOneField(
        Campus, related_name='official_provider', blank=True, null=True)

    class Meta:
        app_label = "feti"
        verbose_name = 'Provider Official'

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return self.user.username
