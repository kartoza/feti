import itertools
import re
import requests
import tempfile

from requests.exceptions import MissingSchema
from django.core import files
from django.core.management.base import BaseCommand
from feti.models.provider import Provider
from feti.utils import get_soup

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '07/12/16'


def normalize_icon_url(icon_url, website):
    # normilize
    if 'http' not in website:
        website = 'http://' + website

    if 'http' not in icon_url:
        domain = website.split('//')
        if len(domain) > 0:
            domain = domain[1]

        if domain not in icon_url:
            if website.endswith("/"):
                website = website[:-1]
            if icon_url.startswith("/"):
                icon_url = icon_url[1:]
            icon_url = website + '/' + icon_url
    return icon_url


def get_provider_icon(url):
    icon = None
    tags = ["img", "strong", "a", "div", "h1", "p"]
    filters = ["logo", "imgLogo", "main-logo", "brand", "logo_link", "site-title", "logo-main", "zo-header-logo"]

    try:
        html = get_soup(url)
        element = None
        for tag in tags:
            for filter in filters:
                raw_html = html.find(tag, {"class": filter})
                if raw_html:
                    element = raw_html
                    break
            if not element:
                for filter in filters:
                    raw_html = html.find(tag, {"id": filter})
                    if raw_html:
                        element = raw_html
                        break

        if element:
            src = element.get('src')
            if src:
                icon = src
            else:
                # get image content
                logo = element.find('img')
                if logo:
                    icon = logo.get('src')
                else:
                    try:
                        style = element['style']
                        urls = re.findall('url\((.*?)\)', style)
                        if len(urls) > 0:
                            icon = urls[0]
                    except KeyError:
                        pass

    except ConnectionResetError:
        pass
    return icon


class Command(BaseCommand):
    args = '<args>'

    def handle(self, *args, **options):
        for provider in Provider.objects.all():
            website = provider.website
            if website and not provider.icon:
                print("getting icon provider %d from %s" % (provider.id, website))
                icon_url = get_provider_icon(website)
                print('raw icon url found = %s' % icon_url)
                if icon_url:
                    try:
                        icon_url = normalize_icon_url(icon_url, website)
                        print('icon url found = %s' % icon_url)
                        # Steam the image from the url
                        request = requests.get(icon_url, stream=True)
                        if request.status_code == requests.codes.ok:
                            print('icon downloaded, save it')
                            # Get the filename from the url, used for saving later
                            file_name = icon_url.split('/')[-1]
                            # Create a temporary file
                            lf = tempfile.NamedTemporaryFile()
                            # Read the streamed image in sections
                            for block in request.iter_content(1024 * 8):
                                # If no more file then stop
                                if not block:
                                    break
                                # Write image block to temporary file
                                lf.write(block)
                            provider.icon.save(file_name, files.File(lf))
                            provider.save()
                    except MissingSchema as e:
                        print(e)
                        print("wrong url %s " % icon_url)
                print("---------------------------")
