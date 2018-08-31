#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `dj-vcn-accounts` models module."""

from dj_vcn_accounts.models import VcnAccount

from django.test import TestCase


class TestVcnAccountModel(TestCase):

    def test_string_representation(self):
        d = {
            "first_name": "Henri",
            "last_name": "Buyse"
        }
        s = VcnAccount(**d)
        self.assertEqual(str(s), "Henri Buyse")

    def test_verbose_name(self):
        self.assertEqual(str(VcnAccount._meta.verbose_name), "VCN account")

    def test_verbose_name_plural(self):
        self.assertEqual(str(VcnAccount._meta.verbose_name_plural), "VCN accounts")

    def test_vcn_account_profile_picture_upload_to_cb(self):
        pass