# -*- coding: utf-8 -*-
"""VCN website user model."""

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class VcnAccount(AbstractUser):
    """User model for the website."""

    staff_title = models.CharField(_('staff title'), max_length=30, blank=True)
    phone = models.CharField(
        _('phone number'),
        max_length=10,
        blank=True,
        validators=[
            # ^
            #     (?:(?:\+|00)33|0)     # Dialing code
            #     \s*[1-9]              # First number (from 1 to 9)
            #     (?:[\s.-]*\d{2}){4}   # End of the phone number
            # $
            RegexValidator(regex=r"^(?:(?:\+|00)33|0)\s*[1-7,9](?:[\s.-]*\d{2}){4}$",
                           message=_("This is not a correct phone number"))
        ]
    )

    def __str__(self):
        """Representation of a VcnAccount as a string."""
        return self.get_full_name()

    class Meta:
        """Meta class."""

        verbose_name = _("VCN account")
        verbose_name_plural = _("VCN accounts")
        ordering = ("first_name", "last_name")
