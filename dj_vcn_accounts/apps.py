# -*- coding: utf-8
"""Representation of the dj-vcn-accounts application and its configuration."""

from django.apps import AppConfig


class DjVcnAccountsConfig(AppConfig):
    """Representation of the dj-vcn-accounts application and its configuration."""

    name = 'dj_vcn_accounts'

    def ready(self):
        """Code to execute when Django starts."""
        import dj_vcn_accounts.signals  # noqa: F401
