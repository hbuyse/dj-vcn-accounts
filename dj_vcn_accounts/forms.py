# coding=utf-8
"""."""

from django.contrib.auth.forms import UserCreationForm

from .models import VcnAccount


class VcnAccountCreationForm(UserCreationForm):
    """Vcn Account creation form."""

    class Meta(UserCreationForm.Meta):
        """Upgrade UserCreationForm with some custom fields."""

        model = VcnAccount
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email',)
