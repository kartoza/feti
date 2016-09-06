# coding=utf-8
from django import template
from user_profile.models.campus_official import CampusOfficial
from user_profile.models.provider_official import ProviderOfficial

__author__ = 'Rizky Maulana Nugraha "lucernae" <lana.pcfre@gmail.com>'
__date__ = '24/04/15'

register = template.Library()


@register.filter
def has_access_user_admin(user):
    output = False
    if user and user.is_authenticated():
        if user.is_staff:
            output = True
        else:
            try:
                CampusOfficial.objects.get(user=user)
                output = True
            except CampusOfficial.DoesNotExist:
                pass
            try:
                ProviderOfficial.objects.get(user=user)
                output = True
            except ProviderOfficial.DoesNotExist:
                pass

    return output
