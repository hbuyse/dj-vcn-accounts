#!/usr/bin/env python
# coding=utf-8

"""Tests for `dj-sponsoring` apps module."""

from dj_vcn_accounts.apps import DjVcnAccountsConfig

from django.apps import apps
from django.test import TestCase


class TestApps(TestCase):

    def test_apps(self):
        self.assertEqual(DjVcnAccountsConfig.name, 'dj_vcn_accounts')
        self.assertEqual(apps.get_app_config('dj_vcn_accounts').name, 'dj_vcn_accounts')
