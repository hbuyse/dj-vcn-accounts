#! /usr/bin/env python

from django.conf import settings
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes

from .models import VcnAccount
from .tokens import (
    account_activation_token
)

import logging
from datetime import datetime, date, timedelta

from .emails import send_activation_email

logger = logging.getLogger(__name__)


@receiver(post_save, sender=VcnAccount)
def post_save_vcnaccount(sender, instance, **kwargs):
    """Post saving function used when saving a VcnAccount

    If the user has just been created, then we send an activation email to be sure that the email works.
    """
    # Add the first breakfast date for a newly created participant.
    logger.debug("post_save_vcnaccount")
    if kwargs['created']:
        send_activation_email(vcnaccount=instance)
