from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models


class Official(models.Model):
    user = models.OneToOneField(User)
    department = models.CharField(max_length=100)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: "
                "'+6288888888888'. Up to 15 digits allowed.")
    phone = models.CharField(
        validators=[phone_regex], blank=True, max_length=15
    )


