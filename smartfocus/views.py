# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404

from stores.models import Store, StorePage
from zoho.models import Page


def home(request, *args, **kwargs):
    return render(request, 'home.html', dict(
        pages=Page.objects.filter(iframe_url__isnull=True),
        stores=Store.objects.all(),
    ))


def store_page(request, store_id, page_slug, *args, **kwargs):
    store = get_object_or_404(
        Store,
        pk=store_id)

    store_page = get_object_or_404(
        StorePage,
        store=store,
        page__slug=page_slug)

    return render(request, 'store_page.html', dict(
        store=store,
        store_page=store_page,
        page=store_page.page,
    ))


def page(request, page_slug, *args, **kwargs):
    page = Page.objects.get(slug=page_slug)
    return render(request, 'page.html', dict(
        page=page,
    ))
