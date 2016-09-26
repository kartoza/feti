from django.core.management.base import BaseCommand

from feti.models.address import Address
from feti.models.campus import Campus
from feti.models.provider import Provider
from feti.utils import get_soup

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '15/09/16'
__license__ = "GPL"
__copyright__ = 'kartoza.com'


def create_provider(data):
    # save to database
    # provider
    try:
        provider = Provider.objects.get(
            primary_institution=data['primary_institution'])
    except Provider.DoesNotExist:
        provider = Provider()
    provider.primary_institution = data['primary_institution']
    provider.website = data['website']
    provider.save()
    return provider


def create_campus(data, provider):
    try:
        campus = Campus.objects.get(
            campus=data['campus'], provider=provider)
    except Campus.DoesNotExist:
        campus = Campus()
    campus.campus = data['campus']
    campus.provider = provider
    campus.save()
    return campus


def create_address(data, campus):
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


class Command(BaseCommand):
    args = '<args>'

    def handle(self, *args, **options):
        args = list(args)
        if len(args) > 0:
            if args[len(args) - 1].lower() == "true":
                Address.objects.all().delete()
                Campus.objects.all().delete()
                Provider.objects.all().delete()
                args.pop(len(args) - 1)
            elif args[len(args) - 1].lower() == "false":
                args.pop(len(args) - 1)
        # ----------------------------------------------------------
        # http://ncap.careerhelp.org.za/
        # ----------------------------------------------------------
        page = 1
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
                        # find detail for campus and provider
                        provider = {}
                        campus = {}
                        address = {}

                        # parsing information
                        name = div.a.string
                        print("found : %s ----------------------------------------" % name)
                        provider['primary_institution'] = name.split('-')[0]
                        campus['campus'] = name.split('-')[1] if name.split('-')[1] else ""

                        # address
                        html = get_soup(div.a.get('href'))
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

                        print(("provider : %s" % provider).encode('utf-8'))
                        print(("campus : %s" % campus).encode('utf-8'))
                        print(("address : %s" % address).encode('utf-8'))

                        # save to database
                        prov = create_provider(provider)
                        camp = create_campus(campus, prov)
                        addr = create_address(address, camp)

                if is_empty:
                    break
            page += 1
            print("----------------------------------------------------------")
        print("----------------------------------------------------------")
