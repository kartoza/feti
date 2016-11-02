import json
from braces.views import LoginRequiredMixin
from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.core.urlresolvers import reverse_lazy
from feti.models.campus import Campus
from feti.models.campus_course_entry import CampusCourseEntry
from feti.models.course import Course
from user_profile.forms.profile_form import UserEditMultiForm
from user_profile.models import CampusCoursesFavorite

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


class UpdateUserCampusCourseView(LoginRequiredMixin, UpdateView):
    model = User

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.body
        status = ""

        try:
            retrieved_data = json.loads(data.decode("utf-8"))
        except ValueError:
            raise Http404(
                'Error json value'
            )
        campus_id = retrieved_data['campus']
        courses_id = retrieved_data['courses_id']

        # Get campus
        try:
            campus = Campus.objects.get(id=campus_id)
        except Campus.DoesNotExist:
            raise Http404(
                'Campus not found'
            )

        try:
            campus_course = CampusCoursesFavorite.objects.get(
                user=user,
                campus=campus
            )
        except CampusCoursesFavorite.DoesNotExist:
            campus_course = CampusCoursesFavorite.objects.create(
                user=user,
                campus=campus
            )

        for course_id in courses_id:
            # Get course
            try:
                course = Course.objects.get(id=course_id)
            except Course.DoesNotExist:
                continue

            if not campus_course.courses.filter(id=course.id).exists():
                campus_course.courses.add(course)
                status = "added"
            else:
                continue

        return HttpResponse(status)


class DeleteUserCampusView(LoginRequiredMixin, UpdateView):
    model = User

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.body
        status = ""

        # Get campus id from request
        try:
            retrieved_data = json.loads(data.decode("utf-8"))
        except ValueError:
            raise Http404(
                'Error json value'
            )
        campus_id = retrieved_data['campus']
        courses_id = retrieved_data['courses_id']

        # Get campus
        try:
            campus = Campus.objects.get(id=campus_id)
        except Campus.DoesNotExist:
            raise Http404(
                'Campus not found'
            )

        try:
            campus_course = CampusCoursesFavorite.objects.get(
                user=user,
                campus=campus
            )
        except CampusCoursesFavorite.DoesNotExist:
            raise Http404(
                'Campus not found'
            )

        # Delete favorites
        for course_id in courses_id:
            # Get course
            try:
                course = Course.objects.get(id=course_id)
            except Course.DoesNotExist:
                continue

            if campus_course.courses.filter(id=course.id).exists():
                campus_course.courses.remove(course)
                status = "deleted"
            else:
                continue

        if not list(campus_course.courses.all()):
            campus_course.delete()

        return HttpResponse(status)
