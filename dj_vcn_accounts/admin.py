from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import VcnAccount


@admin.register(VcnAccount)
class VcnAccountAdmin(UserAdmin):
    model = VcnAccount

    fieldsets = UserAdmin.fieldsets + (
        ('VCN', {'fields': ('staff_title', 'phone',)}),
    )
