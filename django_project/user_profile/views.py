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


def login(request):
    """
    User registration view.
    """
    username = ''
    error = ''
    if request.method == 'POST':
        next = request.POST.get('next')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        print user
        if user is not None:
            if user.is_active:
                django_login(request, user)
                return redirect(next)
        error = 'invalid username or password'
    elif request.method == 'GET':
        next = request.GET.get('next')
    else:
        next = '/'

    if not next:
        next = '/'

    return render_to_response(
        'login_page.html',
        {
            'username': username,
            'next': next,
            'error': error
        },
        context_instance=RequestContext(request))


def logout(request):
    """
    Log out view
    """
    django_logout(request)
    return redirect('/')
