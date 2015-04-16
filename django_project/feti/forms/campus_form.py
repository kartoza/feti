# -*- coding: utf-8 -*-
"""**Forms used to add new flood status reports**

.. tip::
   The AddFloodStatusReport form class is essentially a model form with the
   addition of related fields village and rw.

"""

__author__ = 'Christian Christelis <christian@kartoza.com>'
__revision__ = '$Format:%H$'
__date__ = '04/2015'
__license__ = "GPL"
__copyright__ = 'kartoza.com'

from django import forms
from feti.models.campus import Campus


class AddForm(forms.ModelForm):
    """This form is used to capture details of a .
    """

    class Meta:
        fields = []
        model = Campus
