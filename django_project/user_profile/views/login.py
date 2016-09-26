from django.contrib.auth import (
    login as django_login,
    authenticate,
    logout as django_logout)
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext


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
