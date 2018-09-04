# -*- coding: utf-8 -*-

"""Views."""

import logging

from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import (
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

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.contrib.auth import login
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage


logger = logging.getLogger('django.contrib.gis')


class VcnAccountListView(ListView):
    """View that returns the list of VCN accounts."""

    model = VcnAccount
    staff = False
    webmaster = False

    def get_queryset(self):
        """Get queryset."""
        qs = VcnAccount.objects.all()

        if self.staff:
            logger.debug("Accessing staff page")
            qs = VcnAccount.objects.filter(is_staff=self.staff)

        if self.webmaster:
            logger.debug("Accessing webmaster page")
            qs = VcnAccount.objects.filter(is_superuser=self.webmaster)

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
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        mail_subject = 'Activate your VCN account.'
        message = render_to_string('dj_vcn_accounts/vcnaccount_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
        return super().form_valid(form)

    def get_success_url(self):
        """Get the URL after the success."""
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
        return reverse('dj-vcn-accounts:detail', kwargs={'slug': self.object.username})


def activate(request, uidb64, token):
    """."""
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


class VcnAccountActivationView(View):
    """..."""
    template_name = 'dj_vcn_accounts/vcnaccount_activated.html'

    def get(self, request, *args, **kwargs):
        """..."""
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            # return redirect('home')
            return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        else:
            messages.error(request, "Activation link is invalid!")
            return HttpResponse('Activation link is invalid!')


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
            logger.error("Anonymous user tried to POST to the DeleteView of {}'s account.".format(self.object.username))
            raise PermissionDenied
        elif request.user.id != self.object.id:
            logger.error("User {} tried to POST to the DeleteView of {}'s account.".format(
                request.user.username, self.object.username))
            raise PermissionDenied

        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        """Get the URL after the success."""
        return reverse('dj-vcn-accounts:list')
