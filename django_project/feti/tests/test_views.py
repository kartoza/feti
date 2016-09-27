# coding=utf-8
"""Module related to test for all the models."""
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from core.model_factories import UserFactory
from feti.tests.model_factories import (
    CampusFactory,
    ProviderFactory
)


class TestCampusViews(TestCase):
    """Tests that Campus views work."""

    def setUp(self):
        self.client = Client()
        self.user = UserFactory.create(**{
            'username': 'dimas',
            'password': 'password',
            'is_staff': True
        })
        self.campus = CampusFactory.create()

    def tearDown(self):
        self.user.delete()
        self.campus.delete()

    def test_CampusUpdateView_with_login(self):
        self.client.login(username='dimas', password='password')
        response = self.client.get(reverse('feti:update_campus', kwargs={
            'pk': self.campus.id
        }))
        self.assertEqual(response.status_code, 200)
        expected_templates = [
            'feti/update_campus.html'
        ]
        self.assertEqual(response.template_name, expected_templates)

    def test_CampusUpateView_with_no_login(self):
        response = self.client.get(reverse('feti:update_campus', kwargs={
            'pk': self.campus.id
        }))
        self.assertEqual(response.status_code, 302)


class TestProviderViews(TestCase):
    """Tests that Campus views work."""

    def setUp(self):
        self.client = Client()
        self.user = UserFactory.create(**{
            'username': 'dimas',
            'password': 'password',
            'is_staff': True
        })
        self.provider = ProviderFactory.create()

    def tearDown(self):
        self.user.delete()
        self.provider.delete()

    def test_ProviderUpdateView_with_login(self):
        self.client.login(username='dimas', password='password')
        response = self.client.get(reverse('feti:primary_institute_campus', kwargs={
            'pk': self.provider.id
        }))
        self.assertEqual(response.status_code, 200)
        expected_templates = [
            'feti/update_provider.html'
        ]
        self.assertEqual(response.template_name, expected_templates)

    def test_CampusUpateView_with_no_login(self):
        response = self.client.get(reverse('feti:primary_institute_campus', kwargs={
            'pk': self.provider.id
        }))
        self.assertEqual(response.status_code, 302)
