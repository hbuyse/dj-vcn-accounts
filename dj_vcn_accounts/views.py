# -*- coding: utf-8 -*-

"""Views."""

import logging

from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
    ListView
)

from .models import (
    VcnAccount,
)


logger = logging.getLogger('django.contrib.gis')


class VcnAccountListView(ListView):
    """View that returns the list of VCN accounts."""

    model = VcnAccount
    staff = False

    def get_queryset(self):
        """Get queryset."""
        qs = VcnAccount.objects.all()

        if self.staff:
            logger.debug("Accessing staff page")
            qs = VcnAccount.objects.filter(is_staff=self.staff)

        return qs


class VcnAccountDetailView(DetailView):
    """View that returns the detail of VCN account."""

    model = VcnAccount

    def get_context_data(self, **kwargs):
        """."""
        context = super().get_context_data(**kwargs)
        context['dismissive_alert'] = False
        return context


class VcnAccountCreateView(CreateView):
    """View that creates a new VCN account."""

    model = VcnAccount
    fields = ['username', 'password', 'first_name', 'last_name', 'email', 'staff_title', 'phone']

    def get(self, request, *args, **kwargs):
        """."""
        if request.user.is_authenticated:
            return redirect(reverse("dj-vcn-accounts:update", kwargs={'pk': request.user.id}))
        return super().get(request, args, kwargs)

    def get_success_url(self):
        """Get the URL after the success."""
        return reverse('dj-vcn-accounts:detail', kwargs={'pk': self.object.id})


class VcnAccountUpdateView(UpdateView):
    """View that updates a VCN account."""

    model = VcnAccount
    fields = ['first_name', 'last_name', 'email', 'phone']

    def get(self, request, *args, **kwargs):
        """Override GET method.

        User authenticated and tried to update the informations about an other user -> 403
        User is not authenticated -> 403
        """
        self.object = self.get_object()

        if not request.user.is_authenticated:
            raise PermissionDenied
        elif request.user.id != self.object.id:
            raise PermissionDenied

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Override POST method.

        User authenticated and tried to update the informations about an other user -> 403
        User is not authenticated -> 403
        """
        self.object = self.get_object()

        if not request.user.is_authenticated:
            raise PermissionDenied
        elif request.user.id != self.object.id:
            raise PermissionDenied

        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        """Get the URL after the success."""
        return reverse('dj-vcn-accounts:detail', kwargs={'pk': self.object.id})


class VcnAccountDeleteView(DeleteView):
    """View that deletes a VCN account."""

    model = VcnAccount

    def get_success_url(self):
        """Get the URL after the success."""
        return reverse('dj-vcn-accounts:list')
