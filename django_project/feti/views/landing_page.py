# coding=utf-8
"""FETI landing page view."""

__author__ = 'Christian Christelis <christian@kartoza.com>'
__date__ = '04/2015'
__license__ = "GPL"
__copyright__ = 'kartoza.com'

from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext


def landing_page(request):
    """Serves the FETI landing page.

    :param request: A django request object.
    :type request: request

    :returns: Returns the landing page.
    :rtype: HttpResponse
    """
    return render(
        request,
        'feti/feti.html',
        context_instance=RequestContext(request, {}))
