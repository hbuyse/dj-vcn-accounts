# -*- coding: utf-8
from django.apps import AppConfig


class DjVcnAccountsConfig(AppConfig):
    name = 'dj_vcn_accounts'

    def ready(self):
        import dj_vcn_accounts.signals
