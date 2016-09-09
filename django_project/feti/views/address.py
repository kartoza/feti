from braces.views import LoginRequiredMixin
from feti.models.address import Address
from feti.forms.address_form import AddressForm
from extra_views import InlineFormSet

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '09/08/16'
__license__ = "GPL"
__copyright__ = 'kartoza.com'


class UpdateAddressView(LoginRequiredMixin, InlineFormSet):
    model = Address
    context_object_name = 'administrator'
    form_class = AddressForm
    can_delete = False
