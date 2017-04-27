# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from django.contrib import admin

from . import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', views.home,
        name='home'),

    url(r'^stores/(?P<store_id>\d+)/(?P<page_slug>[-\w]+)/$', views.store_page,
        name='store_page'),

    url(r'^(?P<page_slug>\d+)/$', views.page,
        name='page'),
]
