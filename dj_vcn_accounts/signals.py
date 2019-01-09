# -*- coding: utf-8 -*-
"""Signals handlers for the dj-vcn-accounts."""

import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from .emails import send_activation_email
from .models import VcnAccount

logger = logging.getLogger(__name__)


@receiver(post_save, sender=VcnAccount)
def post_save_vcnaccount(sender, instance, **kwargs):
    """Post saving function used when saving a VcnAccount.

    If the user has just been created, then we send an activation email to be sure that the email works.
    """
    # Add the first breakfast date for a newly created participant.
    logger.debug("post_save_vcnaccount")
    if kwargs['created']:
        send_activation_email(vcnaccount=instance)
