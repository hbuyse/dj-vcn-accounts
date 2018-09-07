#! /usr/bin/env python
# coding=utf-8

"""Tests the views."""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class TestVcnAccountDetailViewAsAnonymous(TestCase):
    """Tests DetailView for Post."""

    def test_get_not_existing(self):
        """Tests."""
        r = self.client.get(reverse('dj-vcn-accounts:detail', kwargs={'slug': 'toto'}))

        self.assertEqual(r.status_code, 404)

    def test_get(self):
        """Teget."""
        u = get_user_model().objects.create_user(username="toto", first_name="Toto", last_name="Toto")

        r = self.client.get(reverse('dj-vcn-accounts:detail', kwargs={'slug': u.get_username()}))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.context['vcnaccount'], u)


class TestVcnAccountDetailViewAsLogged(TestCase):
    """Tests DetailView for Post."""

    def setUp(self):
        """Tests."""
        self.dict = {
            'username': "hbuyse",
            'password': "usermodel",
            'first_name': "Henri",
            'last_name': "Buyse"
        }
        get_user_model().objects.create_user(**self.dict)

    def test_get_not_existing(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('dj-vcn-accounts:detail', kwargs={'slug': 'toto'}))

        self.assertEqual(r.status_code, 404)

    def test_get(self):
        """Tests."""
        u = get_user_model().objects.create_user(username="toto", first_name="Toto", last_name="Toto")

        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('dj-vcn-accounts:detail', kwargs={'slug': u.get_username()}))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.context['vcnaccount'], u)


class TestVcnAccountDetailViewAsStaff(TestCase):
    """Tests DetailView for Post."""

    def setUp(self):
        """Tests."""
        self.dict = {
            'username': "hbuyse",
            'password': "usermodel",
            'first_name': "Henri",
            'last_name': "Buyse",
            'is_staff': True
        }
        get_user_model().objects.create_user(**self.dict)

    def test_get_not_existing(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('dj-vcn-accounts:detail', kwargs={'slug': 'toto'}))

        self.assertEqual(r.status_code, 404)

    def test_get(self):
        """Tests."""
        u = get_user_model().objects.create_user(username="toto", first_name="Toto", last_name="Toto")

        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('dj-vcn-accounts:detail', kwargs={'slug': u.get_username()}))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.context['vcnaccount'], u)


class TestVcnAccountDetailViewAsSuperuser(TestCase):
    """Tests DetailView for Post."""

    def setUp(self):
        """Tests."""
        self.dict = {
            'username': "hbuyse",
            'password': "usermodel",
            'first_name': "Henri",
            'last_name': "Buyse",
            'email': 'toto@example.com'
        }
        get_user_model().objects.create_superuser(**self.dict)

    def test_get_not_existing(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('dj-vcn-accounts:detail', kwargs={'slug': 'toto'}))

        self.assertEqual(r.status_code, 404)

    def test_get(self):
        """Tests."""
        u = get_user_model().objects.create_user(username="toto", first_name="Toto", last_name="Toto")

        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('dj-vcn-accounts:detail', kwargs={'slug': u.get_username()}))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.context['vcnaccount'], u)
