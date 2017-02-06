__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '09/01/17'
import os
import re
import requests
import tempfile

from requests.exceptions import MissingSchema
from django.contrib.gis.geos import GEOSGeometry
from django.core import files

from feti.models.address import Address
from feti.models.campus import Campus
from feti.models.provider import Provider
from feti.utils import get_soup


def normalize_icon_url(icon_url, website):
    """Normilize icon url that found.

    :param icon_url: icon_url that found
    :type icon_url: str

    :param website: of provider
    :type website: str

    :return: normilized url
    :rtype: str
    """
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
    """Getting icon url of provider.

    :param url: url that found
    :type url: str

    :return: icon url that found
    :rtype: str
    """
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

    except (ConnectionResetError, ValueError):
        pass
    return icon


def download_provider_icon(provider):
    """Download provider icon from url that found.

    :param provider: provider that will be updated
    :type provider: Provider
    """
    website = provider.website
    if website and not provider.icon:
        print("getting icon provider %s from %s" % (provider, website))
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
            except MissingSchema as e:
                print(e)
                print("wrong url %s " % icon_url)
        print("---------------------------")


def create_provider(data):
    """Create provider based on data.

    :param data: data provider that found
    :type data: dict

    :return: provider object that created
    :rtype: Provider
    """
    try:
        provider = Provider.objects.get(
            primary_institution=data['primary_institution'])
    except Provider.DoesNotExist:
        provider = Provider()
    provider.primary_institution = data['primary_institution']
    provider.website = data['website']
    # get icon
    download_provider_icon(provider)
    provider.save()
    return provider


def create_campus(data, provider):
    """Create campus based on data.

    :param data: data campus that found
    :type data: dict

    :param provider: provider object that will be used
    :type provider: Provider

    :return: campus object that created
    :rtype: Campus
    """
    try:
        campus = Campus.objects.get(
            campus=data['campus'], provider=provider)
    except Campus.DoesNotExist:
        campus = Campus()
    campus.campus = data['campus']
    campus.provider = provider
    if 'location' in data:
        campus.location = GEOSGeometry(
            'POINT(%s %s)' % (data['location']['lng'], data['location']['lat']))
    campus.save()
    return campus


def create_address(data, campus):
    """Create address based on data for campus.

    :param data: data address that found
    :type data: dict

    :param campus: campus object that will be used
    :type campus: Campus

    :return: address object that created
    :rtype: Address
    """
    try:
        address = Address.objects.get(
            campus_fk=campus)
    except Address.DoesNotExist:
        address = Address()
    address.address_line_1 = data['address_line_1']
    address.town = data['town'] if "town" in data else None
    address.postal_code = data['postal_code'] if "postal_code" in data else None
    address.campus_fk = campus
    address.save()
    return address


def scrap_campus(campus_name, campus_url):
    """Scrap for detail of campus.

    :param campus_name: campus_name that found
    :type campus_name: str

    :param campus_url: campus_url that found
    :type campus_url: str

    :return: campus object that created
    :rtype: Campus
    """
    provider = {}
    campus = {}
    address = {}

    # parsing information
    name = campus_name
    print("found : %s ----------------------------------------" % name)
    provider['primary_institution'] = name.split(' - ')[0]
    try:
        campus['campus'] = name.split('-')[1]
    except IndexError:
        campus['campus'] = ""

    # address
    html = get_soup(campus_url)
    html_address = html.find("div", {"class": "InstitutionAddress"})
    if html_address:
        website = html_address.a.string if html_address.a and "@" not in html_address.a.string else ""
        provider['website'] = website or 'N/A'

        content = str(html_address)
        # get telephone
        telephone = content.split("Telephone")
        if len(telephone) > 1:
            telephone = telephone[1].replace(":", "").strip().split("<")[0]
            address['phone'] = telephone

        # get street address
        content = html_address.get_text()
        street = content.split("Street Address")
        if len(street) > 1:
            street = street[1].split("Postal Address")[0].strip()
            street = street.split("\r\n")
            try:
                postal_code = int(street[len(street) - 1])
            except ValueError:
                postal_code = None
            # get postal code
            if postal_code:
                address['postal_code'] = postal_code
                del street[-1]
            # get town
            if len(street) > 1:
                address['town'] = street[len(street) - 1]
                del street[-1]
            address['address_line_1'] = ", ".join(street)

        # get location
        js_scripts = html.findAll("script", {"type": "text/javascript"})
        for script in js_scripts:
            if script.text != "" and 'mapDiv' in script.text:
                try:
                    locations = {
                        'lat': script.text.split('\r\n')[1].split(',')[1],
                        'lng': script.text.split('\r\n')[1].split(',')[2]
                    }
                    campus['location'] = locations
                except IndexError:
                    print('no location')

    # save to database
    provider_obj = create_provider(provider)
    campus_obj = create_campus(campus, provider_obj)
    address_obj = create_address(address, campus_obj)
    return campus_obj


def scrap_campuses(start_page=0, max_page=0):
    """Scraping campus from off site source.

    :param start_page: start page to be scraped
    :type start_page: int

    :param max_page: max page to be scraped
    :type max_page: int
    """
    # ----------------------------------------------------------
    # http://ncap.careerhelp.org.za/
    # ----------------------------------------------------------
    page = 1

    if start_page > 1:
        page = start_page

    if max_page < start_page:
        return

    print("GETTING CAMPUSS AND PROVIDE IN http://ncap.careerhelp.org.za/")
    print("----------------------------------------------------------")
    while True:
        # get all of list
        print("processing page %d" % page)
        html = get_soup('http://ncap.careerhelp.org.za/learningproviders/search/all/page/%d' % page)
        items = html.findAll("div", {"class": "SearchResultItem"})
        if len(items) == 0:
            # if no item
            break
        elif len(items) >= 1:
            is_empty = True
            # tracing each of item
            for item in items:
                div = item.find("div", {"class": "LinkResult"})
                if div:
                    is_empty = False
                    scrap_campus(div.a.string, div.a.get('href'))
            if is_empty:
                break
        page += 1
        if page > max_page > 0:
            break
        print("----------------------------------------------------------")
    print("----------------------------------------------------------")


def scrap_icons(replace=False):
    """Scraping icon of campus.

    :param replace: replace curent icon or not
    :type replace: bool
    """
    for provider in Provider.objects.all().order_by('primary_institution'):
        if replace:
            provider.clear_icon()

        download_provider_icon(provider)
        provider.save()
