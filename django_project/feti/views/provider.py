from braces.views import LoginRequiredMixin
from django.views.generic import UpdateView
from django.core.urlresolvers import reverse
from django.http import Http404
from feti.models.provider import Provider
from feti.forms.provider_form import ProviderForm

from user_profile.models.provider_official import ProviderOfficial

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '09/08/16'
__license__ = "GPL"
__copyright__ = 'kartoza.com'


class UpdateProviderView(LoginRequiredMixin, UpdateView):
    context_object_name = 'administrator'
    template_name = 'feti/update_provider.html'
    form_class = ProviderForm

    def get_form(self, form_class):
        form = super(UpdateProviderView, self).get_form(form_class)
        return form

    def get_form_kwargs(self):
        kwargs = super(UpdateProviderView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_success_url(self):
        return reverse('user_profile:user-admin-page')

    def get_queryset(self):
        # checking permission
        pk = self.kwargs.get('pk', None)
        provider = None
        if self.request.user.is_authenticated():
            if self.request.user.is_staff:
                provider = Provider.objects.get(pk=pk)
            else:
                try:
                    provider_official = ProviderOfficial.objects.get(user=self.request.user)
                    provider = provider_official.provider.get(pk=pk)
                except ProviderOfficial.DoesNotExist:
                    pass
                except Provider.DoesNotExist:
                    pass

        if not provider:
            raise Http404
        provider = Provider.objects.filter(pk=provider.pk)
        return provider
