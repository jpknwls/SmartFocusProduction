# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.shortcuts import render
from django.shortcuts import redirect
from django import http

from stores.models import StorePage
from stores.views import require_store_association

from zoho.models import Page
from zoho.models import CUSTOM_PAGE_TEMPLATE_ROOT
from zoho.views import require_page_visibility


@require_store_association
@require_page_visibility
def home(request, visible_pages, active_store, associated_stores, *args, **kwargs):
    """
    Main page with nav showing links to different pages.
    """
    return render(request, 'home.html', dict(
        pages=_pages_by_slug(Page.objects.all()),
        visible_pages=_pages_by_slug(visible_pages),
        managed_stores=associated_stores,
        active_store=active_store,
    ))


@require_store_association
@require_page_visibility
def store_page(request,
               active_page, visible_pages,
               active_store, associated_stores,
               *args, **kwargs):
    """
    Renders page identified by ``page_slug``
    and associated with the store identified by ``store_id``.

    Decorators take care of fetching the objects.
    """
    if not active_page:
        raise http.Http404()

    try:
        store_page_obj = StorePage.objects.get(
            store=active_store,
            page=active_page)
    except StorePage.DoesNotExist:
        urls = []
    else:
        urls = store_page_obj.iframe_urls.split('\n')

    title = "{page_title} — {store_name}".format(
        page_title=active_page.title,
        store_name=active_store.name)

    return render(request, 'iframe_page.html', dict(
        pages=_pages_by_slug(Page.objects.all()),
        visible_pages=_pages_by_slug(visible_pages),
        page=active_page,
        active_page=active_page,
        title=title,
        iframe_urls=urls,

        managed_stores=associated_stores,
        active_store=active_store,
    ))


@require_store_association
@require_page_visibility
def page(request,
         active_page, visible_pages,
         active_store, associated_stores,
         *args, **kwargs):
    """
    Renders page identified by ``page_slug``.

    That page must not require store: ``iframe_urls`` must be populated
    with a list of URLs, or it should contain filename of an existing template.
    If neither, it would be rendered empty.

    Decorators take care of fetching the objects.
    """
    if not active_page:
        raise http.Http404()

    if active_page.level == 'STORE_LEVEL':
        return redirect('store_page', active_store.id, active_page.slug)

    urls = active_page.iframe_urls.split('\n')

    custom_template_path = os.path.join(
        CUSTOM_PAGE_TEMPLATE_ROOT,
        active_page.iframe_urls)

    templates_to_try = [
        custom_template_path,
        'iframe_page.html',
    ]
    if request.path.find('salescomparison') != -1:
        templates_to_try = [
        custom_template_path,
        'comparison_page.html',
        ]  

    return render(request, templates_to_try, dict(
        pages=_pages_by_slug(Page.objects.all()),
        visible_pages=_pages_by_slug(visible_pages),
        page=active_page,
        active_page=active_page,
        title=active_page.title,
        iframe_urls=urls,

        managed_stores=associated_stores,
        active_store=active_store,
    ))


def _pages_by_slug(pages):
    data = {}
    for obj in pages:
        data[obj.slug] = dict(
            pk=obj.pk,
            slug=obj.slug,
            icon_path=obj.icon_path,
            title=obj.title,
            description=obj.description,
            level=obj.level,
        )
    return data
