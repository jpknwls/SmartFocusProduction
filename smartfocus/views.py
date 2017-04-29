# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django import http

from stores.models import Store, StorePage, get_managed_stores
from stores.views import require_store_manager
from zoho.models import Page


def home(request, *args, **kwargs):
    """
    Main page.
    Redirects to store home for the first store among managed by current user.
    """
    store = get_managed_stores(request.user)[0]
    return http.HttpResponseRedirect(reverse('store_home', store.pk))


@require_store_manager
def store_home(request, store_id, *args, **kwargs):
    """
    Main page of the store identified by ``store_id``.
    Includes links to store-specific pages as well as chain-wide pages.
    """
    return render(request, 'home.html')


@require_store_manager
def store_page(request, store_id, page_slug, *args, **kwargs):
    """
    Renders page identified by ``page_slug``
    and associated with the store identified by ``store_id``.
    """
    store = get_object_or_404(Store, pk=store_id)

    store_page = get_object_or_404(
        StorePage,
        store=store,
        page__slug=page_slug)

    urls = store_page.iframe_urls.split('/n')

    title = "{page_title} — {store_name}".format(
        page_title=store_page.page.title,
        store_name=store.name)

    return render_page(request, title=title, iframe_urls=urls)


def page(request, page_slug, *args, **kwargs):
    """
    Renders page identified by ``page_slug``.
    That page must not require store (``iframe_urls`` must be populated).
    """
    page = get_object_or_404(Page, slug=page_slug)

    urls = page.iframe_urls.split('/n')

    return render_page(request, title=page.title, iframe_urls=urls)


def render_page(request, title, iframe_urls):
    """
    Renders page template, passing it the following context:

    * ``title`` for window title
    * ``iframe_urls`` for the list of Zoho views to include
    """
    return render(request, 'page.html', dict(
        title=title,
        iframe_urls=iframe_urls,
    ))
