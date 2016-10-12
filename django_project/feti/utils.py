__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '16/09/16'
__license__ = "GPL"
__copyright__ = 'kartoza.com'

import re
import urllib
from bs4 import BeautifulSoup
from urllib.error import HTTPError, URLError


def cleaning(text):
    text = text.replace("\r", "").replace("\n", " ").replace("\t", "").strip()
    return re.sub(' +', ' ', text)


def beautify(html_doc):
    soup = BeautifulSoup(html_doc, 'html.parser')
    return soup


def get_soup(url):
    trying = 0
    html_doc = ''
    while True:
        try:
            html_doc = urllib.request.urlopen(url)
            break
        except (HTTPError, URLError):
            trying += 1
            print("connection error, trying again - %d" % trying)
            if trying >= 5:
                break
    return beautify(html_doc)
