#!/usr/bin/env python
# coding=utf-8

"""Tests for `dj-vcn-accounts` urls module."""

from django.test import TestCase
from django.urls import reverse


class TestUrlsVcnAccount(TestCase):
    """Tests the urls for the dj-vcn-accounts."""

    def test_vcn_account_list_url(self):
        """Test the URL of the listing of VCN accounts."""
        url = reverse('dj-vcn-accounts:list')
        self.assertEqual(url, '/')

    def test_staff_vcn_account_list_url(self):
        """Test the URL of the listing of VCN accounts."""
        url = reverse('dj-vcn-accounts:staff')
        self.assertEqual(url, '/staff')

    def test_vcn_account_create_url(self):
        """Test the URL of that allows the creation of a VCN account."""
        url = reverse('dj-vcn-accounts:create')
        self.assertEqual(url, '/create')

    def test_vcn_account_activate_url(self):
        """Test the URL of that allows the activation of a VCN account."""
        url = reverse('dj-vcn-accounts:activate', kwargs={'uidb64': "123456", "token": "1234567890"})
        self.assertEqual(url, '/activate/123456/1234567890')

    def test_vcn_account_detail_url(self):
        """Test the URL that gives the details of a VCN account."""
        url = reverse('dj-vcn-accounts:detail', kwargs={'slug': 'toto'})
        self.assertEqual(url, '/toto')

    def test_vcn_account_update_url(self):
        """Test the URL of the listing of VCN accounts."""
        url = reverse('dj-vcn-accounts:update', kwargs={'slug': 'toto'})
        self.assertEqual(url, "/toto/update")

    def test_vcn_account_delete_url(self):
        """Test the URL of the listing of VCN accounts."""
        url = reverse('dj-vcn-accounts:delete', kwargs={'slug': 'toto'})
        self.assertEqual(url, "/toto/delete")
