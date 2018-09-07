#! /usr/bin/env python
# coding=utf-8

"""Tests the views."""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class TestVcnAccountDeleteViewAsAnonymous(TestCase):
    """Tests."""

    def setUp(self):
        """Tests."""
        self.dict = {
            'username': "hbuyse",
            'password': "usermodel",
            'first_name': "Henri",
            'last_name': "Buyse"
        }
        self.user = get_user_model().objects.create_user(**self.dict)

    def test_get(self):
        """Tests."""
        r = self.client.get(reverse('dj-vcn-accounts:delete', kwargs={'slug': self.user.get_username()}))
        self.assertEqual(r.status_code, 403)

    def test_post(self):
        """Tests."""
        r = self.client.post(reverse('dj-vcn-accounts:delete', kwargs={'slug': self.user.get_username()}))
        self.assertEqual(r.status_code, 403)


class TestVcnAccountDeleteViewAsLogged(TestCase):
    """Tests."""

    def setUp(self):
        """Tests."""
        self.dict = {
            'username': "hbuyse",
            'password': "usermodel",
            'first_name': "Henri",
            'last_name': "Buyse"
        }
        self.user = get_user_model().objects.create_user(**self.dict)

    def test_get_not_own_account(self):
        """Tests."""
        u = get_user_model().objects.create_user(username="toto", password="toto")

        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('dj-vcn-accounts:delete', kwargs={'slug': u.get_username()}))

        self.assertEqual(r.status_code, 403)

    def test_post_not_own_account(self):
        """Tests."""
        u = get_user_model().objects.create_user(username="toto", password="toto")

        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.post(reverse('dj-vcn-accounts:delete', kwargs={'slug': u.get_username()}), self.dict)

        self.assertEqual(r.status_code, 403)

    def test_get_own_account(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('dj-vcn-accounts:delete', kwargs={'slug': self.user.get_username()}))

        self.assertEqual(r.status_code, 200)

    def test_post_own_account(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.post(reverse('dj-vcn-accounts:delete',
                                     kwargs={'slug': self.user.get_username()}), data=self.dict)

        self.assertEqual(r.status_code, 302)
        self.assertEqual(r.url, reverse('dj-vcn-accounts:list'))


class TestVcnAccountDeleteViewAsStaff(TestCase):
    """Tests."""

    def setUp(self):
        """Tests."""
        self.dict = {
            'username': "hbuyse",
            'password': "usermodel",
            'first_name': "Henri",
            'last_name': "Buyse",
            'is_staff': True
        }
        self.user = get_user_model().objects.create_user(**self.dict)

    def test_get_not_own_account(self):
        """Tests."""
        u = get_user_model().objects.create_user(username="toto", password="toto")
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))

        r = self.client.get(reverse('dj-vcn-accounts:delete', kwargs={'slug': u.get_username()}))
        self.assertEqual(r.status_code, 200)

    def test_post_not_own_account(self):
        """Tests."""
        u = get_user_model().objects.create_user(username="toto", password="toto")
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))

        r = self.client.post(reverse('dj-vcn-accounts:delete', kwargs={'slug': u.get_username()}), self.dict)
        self.assertEqual(r.status_code, 302)
        self.assertEqual(r.url, reverse('dj-vcn-accounts:list'))

    def test_get_own_account(self):
        """Tests."""
        self.assertTrue(self.user.is_active)
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))

        r = self.client.get(reverse('dj-vcn-accounts:delete', kwargs={'slug': self.user.get_username()}))
        self.assertEqual(r.status_code, 200)

    def test_post_own_account(self):
        """Tests."""
        self.assertTrue(self.user.is_active)
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))

        r = self.client.post(reverse('dj-vcn-accounts:delete',
                                     kwargs={'slug': self.user.get_username()}), data=self.dict)
        self.assertEqual(r.status_code, 302)
        self.assertEqual(r.url, reverse('dj-vcn-accounts:list'))


class TestVcnAccountDeleteViewAsSuperuser(TestCase):
    """Tests."""

    def setUp(self):
        """Tests."""
        self.dict = {
            'username': "hbuyse",
            'password': "usermodel",
            'first_name': "Henri",
            'last_name': "Buyse",
            'email': 'toto@example.com'
        }
        self.user = get_user_model().objects.create_superuser(**self.dict)

    def test_get_not_own_account(self):
        """Tests."""
        u = get_user_model().objects.create_user(username="toto", password="toto")
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))

        r = self.client.get(reverse('dj-vcn-accounts:delete', kwargs={'slug': u.get_username()}))
        self.assertEqual(r.status_code, 200)

    def test_post_not_own_account(self):
        """Tests."""
        u = get_user_model().objects.create_user(username="toto", password="toto")
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))

        r = self.client.post(reverse('dj-vcn-accounts:delete', kwargs={'slug': u.get_username()}), self.dict)
        self.assertEqual(r.status_code, 302)
        self.assertEqual(r.url, reverse('dj-vcn-accounts:list'))

    def test_get_own_account(self):
        """Tests."""
        self.assertTrue(self.user.is_active)
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))

        r = self.client.get(reverse('dj-vcn-accounts:delete', kwargs={'slug': self.user.get_username()}))
        self.assertEqual(r.status_code, 200)

    def test_post_own_account(self):
        """Tests."""
        self.assertTrue(self.user.is_active)
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))

        r = self.client.post(reverse('dj-vcn-accounts:delete',
                                     kwargs={'slug': self.user.get_username()}), data=self.dict)
        self.assertEqual(r.status_code, 302)
        self.assertEqual(r.url, reverse('dj-vcn-accounts:list'))
