#! /usr/bin/env python
# coding=utf-8

"""Tests the views."""

from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase
from django.urls import reverse


class TestVcnAccountCreateViewAsAnonymous(TestCase):
    """Tests."""

    def test_get(self):
        """Tests."""
        r = self.client.get(reverse('dj-vcn-accounts:create'))

        self.assertEqual(r.status_code, 200)
        self.assertIn('form', r.context)

    def test_post(self):
        """Tests."""
        d = {
            'username': "toto",
            'password1': "usermodel",
            'password2': "usermodel",
            'first_name': "Toto",
            'last_name': "Toto",
            'email': 'toto@example.com'
        }
        self.assertEqual(len(mail.outbox), 0)
        r = self.client.post(reverse('dj-vcn-accounts:create'), d)

        self.assertEqual(r.status_code, 302)
        self.assertIn('/{}'.format(d['username']), r.url)
        self.assertEqual(len(mail.outbox), 1)


class TestVcnAccountCreateViewAsLogged(TestCase):
    """Tests."""

    def setUp(self):
        """Setup for al the following tests."""
        self.dict = {
            'username': "hbuyse",
            'password': "usermodel",
            'first_name': "Henri",
            'last_name': "Buyse"
        }
        self.user = get_user_model().objects.create_user(**self.dict)

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('dj-vcn-accounts:create'))

        self.assertEqual(r.status_code, 302)
        self.assertIn('/{}/update'.format(self.user.get_username()), r.url)

    def test_post(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.post(reverse('dj-vcn-accounts:create'), data=self.dict)

        self.assertEqual(r.status_code, 403)


class TestVcnAccountCreateViewAsSuperuser(TestCase):
    """Tests."""

    def setUp(self):
        """Setup for al the following tests."""
        self.dict = {
            'username': "hbuyse",
            'password': "usermodel",
            'first_name': "Henri",
            'last_name': "Buyse",
            'email': "toto@example.com"
        }
        self.user = get_user_model().objects.create_superuser(**self.dict)

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('dj-vcn-accounts:create'))

        self.assertEqual(r.status_code, 302)
        self.assertIn('/{}/update'.format(self.user.get_username()), r.url)

    def test_post(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.post(reverse('dj-vcn-accounts:create'), data=self.dict)

        self.assertEqual(r.status_code, 403)
