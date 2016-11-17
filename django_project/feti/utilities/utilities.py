# -*- coding: UTF-8 -*-
__author__ = 'Christian Christelis <christian@kartoza.com>'
__date__ = '16/09/16'
import requests


def get_travel_time(origin, destination, response_type='text'):
    """Get the travel time between two positions.

    :param origin: The origin.
    :type origin: basestring
    :param destination: The destination.
    :type destination: basestring
    :param response_type: Type of response
    :type response_type: basestring

    :return: Travel time in words text or seconds int.
    """
    try:
        from core.settings.secret import GOOGLE_DISTANCE_MATRIX
    except ImportError:
        return

    data = {
        'url': GOOGLE_DISTANCE_MATRIX['url'],
        'units': 'imperial',
        'origins': origin,
        'destinations': destination,
        'key': GOOGLE_DISTANCE_MATRIX['key']}
    url = (
        r'%(url)s?'
        r'units=%(units)s&'
        r'origins=%(origins)s&'
        r'destinations=%(destinations)s&'
        r'key=%(key)s') % data
    response = requests.get(url)
    if not response.ok:
        return None
    rows = response.json()['rows']
    if not rows:
        return None
    if 'elements' not in rows[0]:
        return None
    elements = rows[0]['elements']
    if not elements:
        return None
    if 'duration' not in elements[0]:
        return None
    duration = elements[0]['duration']
    print(response_type)
    print(response_type == 'text')
    if response_type == 'text':
        return duration['text']
    else:
        return duration['value']
