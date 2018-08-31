#!/usr/bin/env python
# coding=utf-8

"""Tests for `dj-vcn-accounts` urls module."""

from django.test import TestCase
from django.urls import reverse


class TestUrlsVcnAccount(TestCase):
    """Tests the urls for the dj-vcn-accounts."""

    def test_vcn_account_list_url(self):
        """Test the URL of the listing of vcn-accounts."""
        url = reverse('dj-vcn-accounts:list')
        self.assertEqual(url, '/')

    def test_staff_vcn_account_list_url(self):
        """Test the URL of the listing of vcn-accounts."""
        url = reverse('dj-vcn-accounts:staff')
        self.assertEqual(url, '/staff')

    def test_vcn_account_create_url(self):
        """Test the URL of that allows the creation of a vcn-account."""
        url = reverse('dj-vcn-accounts:create')
        self.assertEqual(url, '/create')

    def test_vcn_account_detail_url(self):
        """Test the URL that gives the details of a vcn-account."""
        url = reverse('dj-vcn-accounts:detail', kwargs={'pk': 1})
        self.assertEqual(url, '/1')

    def test_vcn_account_update_url(self):
        """Test the URL of the listing of vcn-accounts."""
        url = reverse('dj-vcn-accounts:update', kwargs={'pk': 1})
        self.assertEqual(url, "/1/update")

    def test_vcn_account_delete_url(self):
        """Test the URL of the listing of vcn-accounts."""
        url = reverse('dj-vcn-accounts:delete', kwargs={'pk': 1})
        self.assertEqual(url, "/1/delete")
