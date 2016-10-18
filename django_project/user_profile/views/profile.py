import json
from braces.views import LoginRequiredMixin
from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.core.urlresolvers import reverse_lazy
from feti.models.campus import Campus
from user_profile.forms.profile_form import UserEditMultiForm

__author__ = 'Dimas Ciputra <dimas@kartoza.com>'
__date__ = '21/09/16'


class UserProfileView(LoginRequiredMixin, TemplateView):
    context_object_name = 'profile'
    template_name = 'feti/user_profile.html'

    def get(self, request, *args, **kwargs):
        current_user = request.user
        if current_user.username != self.kwargs.get('username', None):
            raise Http404
        return super(UserProfileView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Get the context data which is passed to a template."""

        context = super(UserProfileView, self).get_context_data(**kwargs)
        username = self.kwargs.get('username', None)

        user = User.objects.get(username=username)

        context['user'] = user

        return context


class UpdateUserProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'feti/update_user_profile.html'
    model = User
    form_class = UserEditMultiForm

    def get_form_kwargs(self):
        kwargs = super(UpdateUserProfileView, self).get_form_kwargs()
        kwargs.update(instance={
            'user': self.object,
            'profile': self.object.profile,
        })
        return kwargs

    def get_success_url(self):
        username = self.object['user'].username
        return reverse_lazy('user_profile:user-profile-view',
                            kwargs={'username': username})


class UpdateUserCampusView(LoginRequiredMixin, UpdateView):
    model = User

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.body

        # Get campus id from request
        try:
            retrieved_data = json.loads(data.decode("utf-8"))
        except ValueError:
            raise Http404(
                'Error json value'
            )
        campus_id = retrieved_data['campus']

        # Get campus
        try:
            campus = Campus.objects.get(id=campus_id)
        except Campus.DoesNotExist:
            raise Http404(
                'Campus not found'
            )

        # Add to favorites
        if not user.profile.campus_favorites.filter(id=campus.id).exists():
            user.profile.campus_favorites.add(campus)
            status = 'added'
        else:
            return HttpResponseForbidden()

        return HttpResponse(status)
