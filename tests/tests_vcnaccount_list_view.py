#! /usr/bin/env python
# coding=utf-8

"""Tests the views."""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class TestVcnAccountListViewAsAnonymous(TestCase):
    """Tests ListView for Post."""

    def tests_list_view_empty(self):
        """Tests."""
        r = self.client.get(reverse('dj-vcn-accounts:list'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['vcnaccount_list']), 0)

    def tests_list_view_one_vcnaccount_not_active(self):
        """Tests."""
        get_user_model().objects.create_user(username="toto",
                                             password="usermodel",
                                             first_name="Toto",
                                             last_name="Toto",
                                             is_active=False)

        r = self.client.get(reverse('dj-vcn-accounts:list'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['vcnaccount_list']), 0)

    def tests_list_view_one_vcnaccount_active(self):
        """Tests."""
        u = get_user_model().objects.create_user(username="toto",
                                                 password="usermodel",
                                                 first_name="Toto",
                                                 last_name="Toto")

        r = self.client.get(reverse('dj-vcn-accounts:list'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['vcnaccount_list']), 1)
        self.assertIn(u.get_full_name(), str(r.content))

    def tests_list_view_one_supervcnaccount_not_active(self):
        """Tests."""
        get_user_model().objects.create_superuser(username="toto",
                                                  password="usermodel",
                                                  first_name="Toto",
                                                  last_name="Toto",
                                                  email="toto@example.com",
                                                  is_active=False)

        r = self.client.get(reverse('dj-vcn-accounts:list'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['vcnaccount_list']), 0)

    def tests_list_view_one_supervcnaccount(self):
        """Tests."""
        u = get_user_model().objects.create_superuser(username="toto",
                                                      password="usermodel",
                                                      first_name="Toto",
                                                      last_name="Toto",
                                                      email="toto@example.com")

        r = self.client.get(reverse('dj-vcn-accounts:list'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['vcnaccount_list']), 1)
        self.assertIn(u.get_full_name(), str(r.content))


class TestVcnAccountListViewAsLogged(TestCase):
    """Tests ListView for Post.

    Note: there is at least one user active in this test. It is the one created in the setUp method.
    """

    def setUp(self):
        """Create a user that will be able to log in."""
        self.dict = {
            'username': "hbuyse",
            'password': "usermodel",
            'first_name': "Henri",
            'last_name': "Buyse"
        }
        self.user = get_user_model().objects.create_user(**self.dict)

    def tests_list_view_one_vcnaccount_not_active(self):
        """Tests."""
        get_user_model().objects.create_user(username="toto",
                                             password="usermodel",
                                             first_name="Toto",
                                             last_name="Toto",
                                             is_active=False)

        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('dj-vcn-accounts:list'))

        self.assertEqual(r.status_code, 200)
        self.assertIn(self.user.get_username(), str(r.content))

    def tests_list_view_one_vcnaccount_active(self):
        """Tests."""
        u = get_user_model().objects.create_user(username="toto",
                                                 password="usermodel",
                                                 first_name="Toto",
                                                 last_name="Toto")

        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('dj-vcn-accounts:list'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(str(r.content).count('<ul>'), 1)
        self.assertEqual(str(r.content).count('<li>'), 2)
        self.assertIn(u.get_full_name(), str(r.content))
        self.assertEqual(str(r.content).count('</li>'), 2)
        self.assertEqual(str(r.content).count('</ul>'), 1)

    def tests_list_view_one_supervcnaccount_not_active(self):
        """Tests."""
        get_user_model().objects.create_superuser(username="toto",
                                                  password="usermodel",
                                                  first_name="Toto",
                                                  last_name="Toto",
                                                  email="toto@example.com",
                                                  is_active=False)

        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('dj-vcn-accounts:list'))

        self.assertEqual(r.status_code, 200)
        self.assertIn(self.user.get_username(), str(r.content))

    def tests_list_view_one_supervcnaccount(self):
        """Tests."""
        u = get_user_model().objects.create_superuser(username="toto",
                                                      password="usermodel",
                                                      first_name="Toto",
                                                      last_name="Toto",
                                                      email="toto@example.com")

        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('dj-vcn-accounts:list'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(str(r.content).count('<ul>'), 1)
        self.assertEqual(str(r.content).count('<li>'), 2)
        self.assertIn(u.get_full_name(), str(r.content))
        self.assertEqual(str(r.content).count('</li>'), 2)
        self.assertEqual(str(r.content).count('</ul>'), 1)


class TestVcnAccountListViewAsSuperuser(TestCase):
    """Tests ListView for Post."""

    def setUp(self):
        """Create a user that will be able to log in."""
        self.dict = {
            'username': "hbuyse",
            'password': "usermodel",
            'first_name': "Henri",
            'last_name': "Buyse",
            'email': 'toto@example.com'
        }
        self.superuser = get_user_model().objects.create_superuser(**self.dict)

    def tests_list_view_one_vcnaccount_not_active(self):
        """Tests."""
        u = get_user_model().objects.create_user(username="toto",
                                                 password="usermodel",
                                                 first_name="Toto",
                                                 last_name="Toto",
                                                 is_active=False)

        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('dj-vcn-accounts:list'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(str(r.content).count('<ul>'), 1)
        self.assertEqual(str(r.content).count('<li>'), 2)
        self.assertIn(u.get_full_name(), str(r.content))
        self.assertEqual(str(r.content).count('</li>'), 2)
        self.assertEqual(str(r.content).count('</ul>'), 1)

    def tests_list_view_one_vcnaccount_active(self):
        """Tests."""
        u = get_user_model().objects.create_user(username="toto",
                                                 password="usermodel",
                                                 first_name="Toto",
                                                 last_name="Toto")

        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('dj-vcn-accounts:list'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(str(r.content).count('<ul>'), 1)
        self.assertEqual(str(r.content).count('<li>'), 2)
        self.assertIn(u.get_full_name(), str(r.content))
        self.assertEqual(str(r.content).count('</li>'), 2)
        self.assertEqual(str(r.content).count('</ul>'), 1)

    def tests_list_view_one_supervcnaccount_not_active(self):
        """Tests."""
        u = get_user_model().objects.create_user(username="toto",
                                                 password="usermodel",
                                                 first_name="Toto",
                                                 last_name="Toto",
                                                 is_active=False)

        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('dj-vcn-accounts:list'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(str(r.content).count('<ul>'), 1)
        self.assertEqual(str(r.content).count('<li>'), 2)
        self.assertIn(u.get_full_name(), str(r.content))
        self.assertEqual(str(r.content).count('</li>'), 2)
        self.assertEqual(str(r.content).count('</ul>'), 1)

    def tests_list_view_one_supervcnaccount(self):
        """Tests."""
        u = get_user_model().objects.create_superuser(username="toto",
                                                      password="usermodel",
                                                      first_name="Toto",
                                                      last_name="Toto",
                                                      email="toto@example.com")

        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('dj-vcn-accounts:list'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(str(r.content).count('<ul>'), 1)
        self.assertEqual(str(r.content).count('<li>'), 2)
        self.assertIn(u.get_full_name(), str(r.content))
        self.assertEqual(str(r.content).count('</li>'), 2)
        self.assertEqual(str(r.content).count('</ul>'), 1)
