from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.sites.models import Site
from django.core.mail import EmailMessage
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

import logging

from .tokens import account_activation_token

logger = logging.getLogger(__name__)

def send_activation_email(vcnaccount):
    from_email = "henri.buyse@gmail.com"
    ctx = {
        'user': vcnaccount,
        'uidb64': urlsafe_base64_encode(force_bytes(vcnaccount.pk)).decode("utf-8"),
        'token': account_activation_token.make_token(vcnaccount)
    }
    if settings.SITE_ID == 1:
        ctx['domain'] = Site.objects.get_current().domain
    else:
        ctx['domain'] = get_current_site(request=None).domain

    subject = render_to_string('dj_vcn_accounts/email/activation_subject.txt', ctx)
    message = render_to_string('dj_vcn_accounts/email/activation_body.txt', ctx)

    logger.info("Sending activation email to {}".format(vcnaccount.email))
    logger.info("Link: 'http://{}{}'".format(ctx['domain'], reverse(
        "dj_vcn_accounts:activate", kwargs={'uidb64': ctx['uidb64'], 'token': ctx['token']})))

    if settings.DEBUG:
        logger.info("Mock: send activation email to {} (to send real email: put settings.DEBUG to True)".format(vcnaccount.email))
    else:
        EmailMessage(subject, message, to=[vcnaccount.email], from_email=from_email).send()
        logger.info("Email sent to {}".format(vcnaccount.email))
