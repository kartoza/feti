from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from feti.models.campus import Campus


class Profile(models.Model):
    user = models.OneToOneField(User)
    bio = models.TextField(max_length=500, blank=True)
    location = models.PointField(blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    campus_favorites = models.ManyToManyField(Campus)

    class Meta:
        app_label = 'feti'
        managed = True


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if Profile.objects.filter(user=instance).exists():
        instance.profile.save()
    else:
        Profile.objects.create(user=instance)
