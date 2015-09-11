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
from django.core.urlresolvers import reverse


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
    else:
        redirect_url = reverse('admin:index')

    if not redirect_url:
        redirect_url = reverse('admin:index')

    return render_to_response(
        'login_page.html',
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
