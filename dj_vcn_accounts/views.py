# -*- coding: utf-8 -*-

"""Views."""

import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import PermissionDenied
from django.core.mail import EmailMessage
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import (
    View,
    CreateView,
    DeleteView,
    UpdateView,
    ListView,
    DetailView
)

from .forms import (
    VcnAccountCreationForm
)
from .models import (
    VcnAccount,
)
from .tokens import (
    account_activation_token
)


logger = logging.getLogger(__name__)


class VcnAccountListView(ListView):
    """View that returns the list of VCN accounts."""

    model = VcnAccount
    staff = False
    webmaster = False

    def get_queryset(self):
        """Get queryset."""

        if not self.request.user.is_superuser:
            qs = VcnAccount.objects.filter(is_active=True)
        else:
            qs = VcnAccount.objects.all()

        if self.staff:
            logger.debug("Accessing staff page")
            qs = qs.filter(is_staff=self.staff)

        if self.webmaster:
            logger.debug("Accessing webmaster page")
            qs = qs.filter(is_superuser=self.webmaster)

        return qs


class VcnAccountDetailView(DetailView):
    """View that returns the detail of VCN account."""

    model = VcnAccount
    # use username instead of pk
    slug_field = "username"

    def get_context_data(self, **kwargs):
        """."""
        context = super().get_context_data(**kwargs)
        context['dismissive_alert'] = False
        return context


class VcnAccountCreateView(CreateView):
    """View that creates a new VCN account."""

    model = VcnAccount
    form_class = VcnAccountCreationForm

    def get(self, request, *args, **kwargs):
        """."""
        if request.user.is_authenticated:
            return redirect(reverse("dj-vcn-accounts:update", kwargs={'slug': request.user.username}))

        return super().get(request, args, kwargs)

    def post(self, request, *args, **kwargs):
        """Override POST method.

        User authenticated and tried to update the informations about an other user -> 403
        User is not authenticated -> 403
        """
        if request.user.is_authenticated:
            raise PermissionDenied

        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        """..."""
        data = {}
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        data['user'] = user
        data['domain'] = get_current_site(self.request).domain
        data['uidb64'] = urlsafe_base64_encode(force_bytes(user.pk)).decode("utf-8")
        data['token'] = account_activation_token.make_token(user)
        logger.info(data)
        logger.info(reverse('dj-vcn-accounts:activate', kwargs={'uidb64': data['uidb64'], 'token': data['token']}))
        email_msg = render_to_string('dj_vcn_accounts/vcnaccount_active_email.html', data)

        logger.info(email_msg)
        to_email = form.cleaned_data.get('email')
        email = EmailMessage('Activate your VCN account.', email_msg, to=[to_email])
        email.send()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        """Get the URL after the success."""
        messages.success("Your account has successfully been created."
                         "Go to your email account to finish the activation.")
        return reverse('dj-vcn-accounts:detail', kwargs={'slug': self.object.username})


class VcnAccountUpdateView(LoginRequiredMixin, UpdateView):
    """View that updates a VCN account."""

    model = VcnAccount
    fields = ['first_name', 'last_name', 'email', 'phone']
    # use username instead of pk
    slug_field = "username"

    def get(self, request, *args, **kwargs):
        """Override GET method.

        User authenticated and tried to update the informations about an other user -> 403
        User is not authenticated -> 403
        """
        self.object = self.get_object()

        # If user is part of staff or superuser
        if request.user.is_staff or request.user.is_superuser:
            logger.info("Staff user {} accessed (GET) the UpdateView of {}'s account.".format(
                request.user.username, self.object.username))
            pass
        # Anonymous user can not update account
        elif not request.user.is_authenticated:
            logger.error("Anonymous user tried to GET the UpdateView of {}'s account.".format(self.object.username))
            raise PermissionDenied
        # Authenticated user can not update an other user account
        elif request.user.id != self.object.id:
            logger.error("User {} tried to GET the UpdateView of {}'s account.".format(
                request.user.username, self.object.username))
            raise PermissionDenied

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Override POST method.

        User authenticated and tried to update the informations about an other user -> 403
        User is not authenticated -> 403
        """
        self.object = self.get_object()

        # If user is part of staff or superuser
        if request.user.is_staff or request.user.is_superuser:
            logger.info("Staff user {} accessed (POST) to the DeleteView of {}'s account.".format(
                request.user.username, self.object.username))
            logger.info(kwargs)
            pass
        elif not request.user.is_authenticated:
            logger.error(
                "Anonymous user tried to POST to the DeleteView of {}'s account.".format(self.object.username)
            )
            raise PermissionDenied
        elif request.user.id != self.object.id:
            logger.error("User {} tried to POST to the DeleteView of {}'s account.".format(
                request.user.username, self.object.username))
            raise PermissionDenied

        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        """Get the URL after the success."""
        messages.success(self.request, "You successfully updated your account.")
        return reverse('dj-vcn-accounts:detail', kwargs={'slug': self.object.username})


class VcnAccountDeleteView(LoginRequiredMixin, DeleteView):
    """View that deletes a VCN account."""

    model = VcnAccount
    # use username instead of pk
    slug_field = "username"

    def get(self, request, *args, **kwargs):
        """Override GET method.

        User authenticated and tried to update the informations about an other user -> 403
        User is not authenticated -> 403
        """
        self.object = self.get_object()

        # If user is part of staff or superuser
        if request.user.is_staff or request.user.is_superuser:
            logger.info("Staff user {} accessed (GET) the DeleteView of {}'s account.".format(
                request.user.username, self.object.username))
            pass
        # Anonymous user can not update account
        elif not request.user.is_authenticated:
            logger.error("Anonymous user tried to GET the DeleteView of {}'s account.".format(self.object.username))
            raise PermissionDenied
        # Authenticated user can not update an other user account
        elif request.user.id != self.object.id:
            logger.error("User {} tried to GET the DeleteView of {}'s account.".format(
                request.user.username, self.object.username))
            raise PermissionDenied

        return super().get(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Override DELETE method (in DeleteView, post function calls delete function).

        User authenticated and tried to update the informations about an other user -> 403
        User is not authenticated -> 403
        """
        self.object = self.get_object()

        # If user is part of staff or superuser
        if request.user.is_staff or request.user.is_superuser:
            logger.info("Staff user {} accessed (DELETE) to the DeleteView of {}'s account.".format(
                request.user.username, self.object.username))
            logger.info(kwargs)
            pass
        elif not request.user.is_authenticated:
            logger.error("Anonymous user tried to delete {}'s account.".format(self.object.username))
            raise PermissionDenied
        elif request.user.id != self.object.id:
            logger.error("User {} tried to delete {}'s account.".format(
                request.user.username, self.object.username))
            raise PermissionDenied

        logger.info("VcnAccount {} deactivated".format(self.object.get_username()))
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        """Get the URL after the success."""
        messages.success(self.request, "You successfully deactivated your account.")
        return reverse('dj-vcn-accounts:list')


class VcnAccountActivationView(View):
    """View handled when the user activates its account.

    See https://medium.com/@frfahim/django-registration-with-confirmation-email-bb5da011e4ef for documentation
    """

    template_name = 'dj_vcn_accounts/vcnaccount_activated.html'

    def get(self, request, *args, **kwargs):
        """..."""
        try:
            user_id = force_text(urlsafe_base64_decode(kwargs['uidb64']))
            user = VcnAccount.objects.get(pk=user_id)
            logging.info("Activation requested for user {}".format(user.get_username()))
        except(TypeError, ValueError, OverflowError, VcnAccount.DoesNotExist) as e:
            logging.exception("Failed to decode user during VcnAccountActivationView: " + str(e))
            user = None

        if user is not None and account_activation_token.check_token(user, kwargs['token']):
            user.is_active = True
            user.save()
        else:
            messages.error(self.request, "Activation link is invalid!")
            raise Http404

        messages.success(self.request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect(reverse("dj_vcn_accounts:list"))
