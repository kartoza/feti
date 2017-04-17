# coding=utf-8
from django.views.generic import TemplateView

__author__ = 'Dimas Ciputra <dimas@kartoza.com>'
__date__ = '17/04/17'


class JasmineView(TemplateView):
    template_name = 'jasmine_page.html'
