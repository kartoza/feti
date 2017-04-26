# coding=utf-8

from braces.views import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.views.generic import CreateView, TemplateView
from feti.models.feedback import Feedback
from feti.forms.feedback_form import FeedbackForm

__author__ = 'Anita Hapsari <anita@kartoza.com>'
__date__ = '25/04/17'


class FeedbackInputView(LoginRequiredMixin, CreateView):
    context_object_name = 'feedback'
    template_name = 'feti/input_feedback.html'
    form_class = FeedbackForm
    model = Feedback

    def get_form(self, form_class):
        form = super(FeedbackInputView, self).get_form(form_class)
        return form

    def get_form_kwargs(self):
        kwargs = super(FeedbackInputView, self).get_form_kwargs()
        return kwargs

    def get_success_url(self):
        return reverse('feti:success_view')


class FeedbackSubmittedView(TemplateView):
    template_name = 'feti/success_view.html'
