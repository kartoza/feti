from braces.views import LoginRequiredMixin
from django.views.generic import UpdateView
from django.core.urlresolvers import reverse
from django.http import Http404
from feti.models.campus import Campus
from feti.forms.campus_form import CampusForm

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '09/08/16'
__license__ = "GPL"
__copyright__ = 'kartoza.com'


class UpdateCampusView(LoginRequiredMixin, UpdateView):
    context_object_name = 'administrator'
    template_name = 'feti/update_campus.html'
    form_class = CampusForm

    def get_form(self, form_class):
        form = super(UpdateCampusView, self).get_form(form_class)
        return form

    def get_form_kwargs(self):
        kwargs = super(UpdateCampusView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_success_url(self):
        return reverse('user-manager', args=(self.request.user,))

    def get_queryset(self):
        if not self.request.user.is_authenticated():
            raise Http404

        # checking permission
        pk = self.kwargs.get('pk', None)
        try:
            campus = Campus.objects.filter(pk=pk)
        except Campus.DoesNotExist:
            raise Http404

        return campus
