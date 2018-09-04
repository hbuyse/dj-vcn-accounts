#! /usr/bin/env python
# coding=utf-8

"""Tests the views."""

from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class TestVcnAccountListView(TestCase):
    """Tests ListView for Post."""

    def tests_list_view_empty(self):
        """Tests."""
        r = self.client.get(reverse('dj-vcn-accounts:list'))
        self.assertEqual(r.status_code, 200)
        self.assertIn("No accounts...", str(r.content))

    def tests_list_view_one_post(self):
        """Tests."""
        u = get_user_model().objects.create_user(username="hbuyse",
                                                 password="usermodel",
                                                 first_name="Henri",
                                                 last_name="Buyse")
        r = self.client.get(reverse('dj-vcn-accounts:list'))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(str(r.content).count('<ul>'), 1)
        self.assertEqual(str(r.content).count('<li>'), 1)
        self.assertIn(u.get_full_name(), str(r.content))
        self.assertEqual(str(r.content).count('</li>'), 1)
        self.assertEqual(str(r.content).count('</ul>'), 1)


class TestVcnAccountDetailView(TestCase):
    """Tests DetailView for Post."""

    def test_detail_view_not_existing(self):
        """Tests."""
        r = self.client.get(reverse('dj-vcn-accounts:detail', kwargs={'slug': 'toto'}))
        self.assertEqual(r.status_code, 404)

    def test_detail_view(self):
        """Tests."""
        u = get_user_model().objects.create_user(username="hbuyse",
                                                 password="usermodel",
                                                 first_name="Henri",
                                                 last_name="Buyse")
        r = self.client.get(reverse('dj-vcn-accounts:detail', kwargs={'slug': u.username}))
        self.assertEqual(r.status_code, 200)
        self.assertIn(u.get_full_name(), str(r.content))
        self.assertIn(u.username, str(r.content))


class TestVcnAccountCreateView(TestCase):
    """Tests."""

    def setUp(self):
        """Setup for al the following tests."""
        self.dict = {
            'username': "hbuyse",
            'password': "usermodel",
            'first_name': "Henri",
            'last_name': "Buyse"
        }

    def test_create_view_get_as_anonymous(self):
        """Tests."""
        r = self.client.get(reverse('dj-vcn-accounts:create'))
        self.assertEqual(r.status_code, 200)

    def test_create_view_post_as_anonymous(self):
        """Tests."""
        r = self.client.post(reverse('dj-vcn-accounts:create'), self.dict)
        self.assertEqual(r.status_code, 302)
        self.assertIn('/{}'.format(self.dict['username']), r.url)

    def test_create_view_get_as_logged(self):
        """Tests."""
        u = get_user_model().objects.create_user(**self.dict)
        self.assertTrue(self.client.login(username=self.dict['username'],
                                          password=self.dict['password']))

        r = self.client.get(reverse('dj-vcn-accounts:create'))
        self.assertEqual(r.status_code, 302)
        self.assertIn('/{}/update'.format(u.username), r.url)

    def test_create_view_post_as_logged(self):
        """Tests."""
        get_user_model().objects.create_user(**self.dict)
        self.assertTrue(self.client.login(username=self.dict['username'],
                                          password=self.dict['password']))

        r = self.client.post(reverse('dj-vcn-accounts:create'), data=self.dict)
        self.assertEqual(r.status_code, 403)


class TestVcnAccountUpdateView(TestCase):
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

    def test_update_view_get_as_anonymous(self):
        """Tests."""
        r = self.client.get(reverse('dj-vcn-accounts:update', kwargs={'slug': self.user.username}))
        self.assertEqual(r.status_code, 403)

    def test_update_view_post_as_anonymous(self):
        """Tests."""
        r = self.client.post(reverse('dj-vcn-accounts:update', kwargs={'slug': self.user.username}), self.dict)
        self.assertEqual(r.status_code, 403)

    def test_update_view_get_as_logged_not_own_account(self):
        """Tests."""
        u = get_user_model().objects.create_user(username="toto", password="toto")
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('dj-vcn-accounts:update', kwargs={'slug': u.username}))
        self.assertEqual(r.status_code, 403)

    def test_update_view_post_as_logged_not_own_account(self):
        """Tests."""
        r = self.client.post(reverse('dj-vcn-accounts:update', kwargs={'slug': self.user.username}), self.dict)
        self.assertEqual(r.status_code, 403)

    def test_update_view_get_as_logged_own_account(self):
        """Tests."""
        self.assertTrue(self.user.is_active)
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))

        r = self.client.get(reverse('dj-vcn-accounts:update', kwargs={'slug': self.user.username}))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(str(r.content).count('<label'), 4)
        self.assertEqual(str(r.content).count('</label>'), 4)
        self.assertIn('First name', str(r.content))
        self.assertIn('Last name', str(r.content))
        self.assertIn('Email', str(r.content))
        self.assertIn('Phone', str(r.content))

    def test_update_view_post_as_logged_own_account(self):
        """Tests."""
        self.assertTrue(self.user.is_active)
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))

        self.dict['first_name'] = 'First'
        r = self.client.post(reverse('dj-vcn-accounts:update', kwargs={'slug': self.user.username}), data=self.dict)
        self.assertEqual(r.status_code, 302)
        self.assertEqual(r.url, reverse('dj-vcn-accounts:detail', kwargs={'slug': self.user.username}))


class TestVcnAccountDeleteView(TestCase):
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

    def test_delete_view_get_as_anonymous(self):
        """Tests."""
        r = self.client.get(reverse('dj-vcn-accounts:delete', kwargs={'slug': self.user.username}))
        self.assertEqual(r.status_code, 403)

    def test_delete_view_post_as_anonymous(self):
        """Tests."""
        r = self.client.post(reverse('dj-vcn-accounts:delete', kwargs={'slug': self.user.username}), self.dict)
        self.assertEqual(r.status_code, 403)

    def test_delete_view_get_as_logged_not_own_account(self):
        """Tests."""
        u = get_user_model().objects.create_user(username="toto", password="toto")
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('dj-vcn-accounts:delete', kwargs={'slug': u.username}))
        self.assertEqual(r.status_code, 403)

    def test_delete_view_post_as_logged_not_own_account(self):
        """Tests."""
        r = self.client.post(reverse('dj-vcn-accounts:delete', kwargs={'slug': self.user.username}), self.dict)
        self.assertEqual(r.status_code, 403)

    def test_delete_view_get_as_logged_own_account(self):
        """Tests."""
        self.assertTrue(self.user.is_active)
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))

        r = self.client.get(reverse('dj-vcn-accounts:delete', kwargs={'slug': self.user.username}))
        self.assertEqual(r.status_code, 200)

    def test_delete_view_post_as_logged_own_account(self):
        """Tests."""
        self.assertTrue(self.user.is_active)
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))

        self.dict['first_name'] = 'First'
        r = self.client.post(reverse('dj-vcn-accounts:delete', kwargs={'slug': self.user.username}), data=self.dict)
        self.assertEqual(r.status_code, 302)
        self.assertEqual(r.url, reverse('dj-vcn-accounts:list'))
