# coding=utf-8
from django import forms
from haystack.forms import SearchForm

__author__ = 'Rizky Maulana Nugraha "lucernae" <lana.pcfre@gmail.com>'
__date__ = '24/04/15'


class DefaultSearchForm(SearchForm):
    status = forms.BooleanField()

    def search(self):
        sqs = super(DefaultSearchForm, self).search()
        return sqs
