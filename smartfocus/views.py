# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

from stores.models import Store, StorePage
from stores.views import require_store_manager
from zoho.models import Page
from zoho.models import CUSTOM_PAGE_TEMPLATE_ROOT


@require_store_manager
def home(request, active_store, managed_stores, *args, **kwargs):
    """
    Main page with nav showing links to different pages.
    """
    return render(request, 'home.html', dict(
        active_store=active_store,
        managed_stores=managed_stores,
    ))


@require_store_manager
def store_page(request, store_id, page_slug,
               active_store, managed_stores,
               *args, **kwargs):
    """
    Renders page identified by ``page_slug``
    and associated with the store identified by ``store_id``.
    """
    store = get_object_or_404(Store, pk=store_id)
    page = get_object_or_404(Page, slug=page_slug)

    try:
        store_page = StorePage.objects.get(store=store, page=page)
    except StorePage.DoesNotExist:
        urls = []
    else:
        urls = store_page.iframe_urls.split('\n')

    title = "{page_title} — {store_name}".format(
        page_title=page.title,
        store_name=store.name)

    return render(request, 'iframe_page.html', dict(
        page=page,
        title=title,
        iframe_urls=urls,
        active_store=active_store,
        managed_stores=managed_stores,
    ))


@require_store_manager
def page(request, page_slug, active_store, managed_stores, *args, **kwargs):
    """
    Renders page identified by ``page_slug``.

    That page must not require store: ``iframe_urls`` must be populated
    with a list of URLs, or it should contain filename of an existing template.
    If neither, it would be rendered empty.
    """
    page = get_object_or_404(Page, slug=page_slug)

    if page.level == 'STORE_LEVEL':
        return redirect('store_page', active_store.id, page_slug)

    custom_template_path = os.path.join(
        CUSTOM_PAGE_TEMPLATE_ROOT,
        page.contents)

    templates_to_try = [
        custom_template_path,
        'iframe_page.html',
    ]

    urls = page.contents.split('\n')

    return render(request, templates_to_try, dict(
        page=page,
        title=page.title,
        iframe_urls=urls,
        active_store=active_store,
        managed_stores=managed_stores,
    ))
