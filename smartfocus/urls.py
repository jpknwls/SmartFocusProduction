# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^login/',
        auth_views.LoginView.as_view(template_name='login.html'),
        name='login'),

    url(r'^logout/',
        auth_views.logout_then_login,
        name='logout'),

    url(r'^$',
        login_required(views.home),
        name='home'),

    # Store-specific pages
    url(r'^stores/(?P<store_id>\d+)$',
        login_required(views.store_home),
        name='store_home'),

    url(r'^stores/(?P<store_id>\d+)/(?P<page_slug>[-\w]+)/$',
        login_required(views.store_page),
        name='store_page'),

    # Chain-wide pages
    url(r'^(?P<page_slug>\d+)/$',
        login_required(views.page),
        name='page'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
