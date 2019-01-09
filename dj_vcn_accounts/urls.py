# -*- coding: utf-8 -*-
"""VCN Accounts URL Configuration.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

"""

from django.urls import path

from . import views


app_name = 'dj-vcn-accounts'

urlpatterns = [
    path('',
         view=views.VcnAccountListView.as_view(),
         name='list'
         ),
    path('staff/',
         view=views.VcnAccountListView.as_view(staff=True),
         name='staff'
         ),
    path('webmaster/',
         view=views.VcnAccountListView.as_view(webmaster=True),
         name='webmaster'
         ),
    path('create/',
         view=views.VcnAccountCreateView.as_view(),
         name='create'
         ),
    path('activate/<slug:uidb64>/<slug:token>/',
         view=views.VcnAccountActivationView.as_view(),
         name='activate'
         ),
    path('<str:slug>/',
         view=views.VcnAccountDetailView.as_view(),
         name='detail'
         ),
    path('<str:slug>/update/',
         view=views.VcnAccountUpdateView.as_view(),
         name='update'
         ),
    path('<str:slug>/delete/',
         view=views.VcnAccountDeleteView.as_view(),
         name='delete'
         ),
]
