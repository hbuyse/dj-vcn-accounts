#! /usr/bin/env python
# coding=utf-8

"""Tests the views."""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from dj_vcn_accounts.tokens import (
    account_activation_token
)


class TestVcnAccountActivationViewAsAnonymous(TestCase):
    """Tests."""

    def setUp(self):
        """Tests."""
        self.dict = {
            'username': "hbuyse",
            'password': "usermodel",
            'first_name': "Henri",
            'last_name': "Buyse",
            'is_active': False
        }
        self.user = get_user_model().objects.create_user(**self.dict)

    def generate_uidb64_token(self, obj):
        """Return a tuple formed of uidb64 and the token."""
        uidb64 = urlsafe_base64_encode(force_bytes(obj.pk)).decode("utf-8")
        token = account_activation_token.make_token(obj)

        return uidb64, token

    def test_get_no_account_to_activate(self):
        """Tests."""
        r = self.client.get(reverse('dj-vcn-accounts:activate', kwargs={'uidb64': '123456', 'token': '1234567890'}))

        self.assertEqual(r.status_code, 404)

    def test_get_account_to_activate_wrong_uidb64(self):
        """Tests."""
        uidb64, token = self.generate_uidb64_token(self.user)
        self.assertFalse(self.user.is_active)

        r = self.client.get(reverse('dj-vcn-accounts:activate', kwargs={'uidb64': uidb64[0:-1], 'token': token}))

        self.assertEqual(r.status_code, 404)
        self.user = get_user_model().objects.get(id=self.user.id)

        # Got the user again because of the user caching
        self.user = get_user_model().objects.get(id=self.user.id)
        self.assertFalse(self.user.is_active)

    def test_get_account_to_activate_wrong_token(self):
        """Tests."""
        uidb64, token = self.generate_uidb64_token(self.user)
        self.assertFalse(self.user.is_active)

        r = self.client.get(reverse('dj-vcn-accounts:activate', kwargs={'uidb64': uidb64, 'token': token[0:-1]}))

        self.assertEqual(r.status_code, 404)
        self.user = get_user_model().objects.get(id=self.user.id)

        # Got the user again because of the user caching
        self.user = get_user_model().objects.get(id=self.user.id)
        self.assertFalse(self.user.is_active)

    def test_get_account_to_activate(self):
        """Tests."""
        uidb64, token = self.generate_uidb64_token(self.user)
        self.assertFalse(self.user.is_active)

        r = self.client.get(reverse('dj-vcn-accounts:activate', kwargs={'uidb64': uidb64, 'token': token}))

        self.assertEqual(r.status_code, 302)
        self.assertEqual(r.url, reverse('dj-vcn-accounts:list'))

        # Got the user again because of the user caching
        self.user = get_user_model().objects.get(id=self.user.id)
        self.assertTrue(self.user.is_active)
