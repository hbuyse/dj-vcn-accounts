# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.urls import include, path
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('login', auth_views.LoginView.as_view(), name='vcn-account-login'),
    path('logout', auth_views.LogoutView.as_view(), {'next_page': '/'}, name='vcn-account-logout'),
    path('', include('dj_vcn_accounts.urls', namespace='dj_vcn_accounts')),
]
