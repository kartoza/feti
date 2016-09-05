# coding=utf-8
"""Custom login/logout views.

author: christian@kartoza.com
date: January 2015
"""
from django.contrib.auth import (
    login as django_login,
    authenticate,
    logout as django_logout)
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.views.generic import TemplateView

from feti.models.campus import Campus
from feti.serializers.campus_serializer import CampusSerializer

from user_profile.models.campus_official import CampusOfficial

from feti.templatetags.user_admin import has_access_user_admin


def login(request):
    """
    User registration view.
    """
    username = ''
    error = ''
    if request.method == 'POST':
        redirect_url = request.POST.get('next')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                django_login(request, user)
                return redirect(redirect_url)
        error = 'invalid username or password'
    elif request.method == 'GET':
        redirect_url = request.GET.get('next')

    if not redirect_url:
        if user.is_superuser or user.is_staff:
            redirect_url = reverse('admin:index')
        else:
            # admin for provider
            redirect_url = reverse('admin:index')

    return render_to_response(
        'login_page.html',
        {
            'username': username,
            'next': redirect_url,
            'error': error
        },
        context_instance=RequestContext(request))


def login_modal(request):
    """
    User login modal view.
    """
    username = ''
    error = ''

    if request.method == 'POST':
        redirect_url = request.POST.get('next')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            django_login(request, user)
            return redirect(redirect_url)
        error = 'invalid username or password'

    if not redirect_url:
        if user.is_superuser or user.is_staff:
            redirect_url = reverse('admin:index')
        else:
            # admin for provider
            redirect_url = reverse('admin:index')

    return render_to_response(
        'feti/landing_page.html',
        {
            'username': username,
            'next': redirect_url,
            'error': error
        },
        context_instance=RequestContext(request))


def logout(request):
    """
    Log out view
    """
    django_logout(request)
    return redirect('/')


class UserAdminPage(TemplateView):
    template_name = 'user_admin_page.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        campus = None
        try:
            # get official detail
            user = request.user
            if has_access_user_admin(user):
                if user.is_staff:
                    campus = CampusSerializer(Campus.objects.all(), many=True).data
                else:
                    official = CampusOfficial.objects.get(user=user)
                    campus = CampusSerializer(official.campus.all(), many=True).data
        except CampusOfficial.DoesNotExist:
            pass

        if campus:
            context['campus'] = campus
            return self.render_to_response(context)
        else:
            raise Http404()
