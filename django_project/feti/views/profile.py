from braces.views import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.http import Http404

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
