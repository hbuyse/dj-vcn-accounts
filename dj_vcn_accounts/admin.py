# -*- coding: utf-8
"""Representation of the dj-vcn-accounts admin pages."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import VcnAccount


@admin.register(VcnAccount)
class VcnAccountAdmin(UserAdmin):
    """VcnAccount administration view."""

    model = VcnAccount

    fieldsets = UserAdmin.fieldsets + (
        ('VCN', {'fields': ('staff_title', 'phone',)}),
    )
