import re
import os
from django.conf import settings
import urllib
import requests
from bs4 import BeautifulSoup
from urllib.error import HTTPError, URLError
from django.core.files import File

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '16/09/16'
__license__ = "GPL"
__copyright__ = 'kartoza.com'


def cleaning(text):
    text = text.replace("\r", "").replace("\n", " ").replace("\t", "").strip()
    return re.sub(' +', ' ', text)


def beautify(html_doc):
    soup = BeautifulSoup(html_doc, 'html.parser')
    return soup


def get_raw_soup(url):
    trying = 0
    html_doc = ''
    while True:
        try:
            html_doc = requests.get(url)
            break
        except (HTTPError, URLError):
            trying += 1
            print("connection error, trying again - %d" % trying)
            if trying >= 5:
                break
    return html_doc


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


def open_saved_html(folder, filename):
    full_filename = os.path.join(settings.MEDIA_ROOT, folder, cleaning(filename) + '.html')
    try:
        with open(full_filename, 'r', encoding='ISO-8859-1') as f:
            return BeautifulSoup(f, 'html.parser')
    except FileNotFoundError:
        return


def save_html(folder, filename, content):

    # create the folder if it doesn't exist.
    try:
        os.mkdir(os.path.join(settings.MEDIA_ROOT, folder))
    except OSError:
        pass

    full_filename = os.path.join(settings.MEDIA_ROOT, folder, filename + '.html')
    with open(full_filename, 'wb') as file:
        file.write(content)
