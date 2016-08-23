# coding=utf-8
"""Custom login/logout views.

author: christian@kartoza.com
date: January 2015
"""
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth import (
    login as django_login,
    authenticate,
    logout as django_logout)
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import Http404
from django.views.generic import TemplateView

from feti.serializers.campus_serializer import CampusSerializer
from models.campus_official import CampusOfficial


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
            if user.is_active:
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


class ProfilePage(TemplateView):
    template_name = 'user_profile_page.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        username = self.kwargs.get('username', None)
        if username:
            try:
                user = User.objects.get(username=username)
                context['username'] = user.username
                context['email'] = user.email
                context['full_name'] = user.get_full_name()

                # get official detail
                official = CampusOfficial.objects.get(user=user)
                context['department'] = official.department
                context['phone'] = official.phone

                if request.user.is_authenticated() and request.user == user:
                    context['campus'] = CampusSerializer(official.campus).data

            except User.DoesNotExist:
                raise Http404("User doesn't exist")
            except CampusOfficial.DoesNotExist:
                pass
        return self.render_to_response(context)
