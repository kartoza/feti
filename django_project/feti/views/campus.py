from braces.views import LoginRequiredMixin
from extra_views import UpdateWithInlinesView
from django.core.urlresolvers import reverse
from django.http import Http404
from feti.models.campus import Campus
from feti.forms.campus_form import CampusForm
from feti.views.address import UpdateAddressView

from user_profile.models.campus_official import CampusOfficial
from user_profile.models.provider_official import ProviderOfficial

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '09/08/16'
__license__ = "GPL"
__copyright__ = 'kartoza.com'


class UpdateCampusView(LoginRequiredMixin, UpdateWithInlinesView):
    context_object_name = 'administrator'
    template_name = 'feti/update_campus.html'
    form_class = CampusForm
    model = Campus
    inlines = [UpdateAddressView]

    def get_form(self, form_class):
        form = super(UpdateCampusView, self).get_form(form_class)
        return form

    def get_form_kwargs(self):
        kwargs = super(UpdateCampusView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_success_url(self):
        return reverse('user_profile:user-admin-page')

    def get_queryset(self):
        # checking permission
        pk = self.kwargs.get('pk', None)
        campus = None
        if self.request.user.is_authenticated():
            if self.request.user.is_staff:
                campus = Campus.objects.get(pk=pk)
            else:
                # checking from provider official
                try:
                    provider_official = ProviderOfficial.objects.get(user=self.request.user)
                    campus = Campus.objects.filter(
                        provider__in=provider_official.provider.all()).get(pk=pk)
                except ProviderOfficial.DoesNotExist:
                    pass
                except Campus.DoesNotExist:
                    pass
                # checking from campus official
                if not campus:
                    try:
                        campus_official = CampusOfficial.objects.get(user=self.request.user)
                        campus = campus_official.campus.get(pk=pk)
                    except CampusOfficial.DoesNotExist:
                        pass
                    except Campus.DoesNotExist:
                        pass

        if not campus:
            raise Http404
        campus = Campus.objects.filter(pk=campus.pk)
        return campus
