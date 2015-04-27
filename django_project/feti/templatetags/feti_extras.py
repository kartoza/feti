# coding=utf-8
__author__ = 'Rizky Maulana Nugraha "lucernae" <lana.pcfre@gmail.com>'
__date__ = '24/04/15'

from django import template

register = template.Library()


@register.filter
def typenamestring(value):
    return value