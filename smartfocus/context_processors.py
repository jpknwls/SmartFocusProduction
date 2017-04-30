# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from stores.models import Store
from stores.models import get_managed_stores
from zoho.models import Page


def managed_stores(request):
    """
    Returns context with stores managed by currently logged-in user.
    """
    if not request.user.is_authenticated():
        return dict()

    return dict(
        managed_stores=
            get_managed_stores(request.user).
            prefetch_related('store_pages'),
    )


def page_navigation(request):
    """
    Returns context with page navigation structures, split by sections.
    """

    # Accumulates all page objects into a dictionary
    # so we can easily pull them by slug when building navigation below
    pages = {}
    for page in Page.objects.all():
        pages[page.slug] = page

    # Little helper to get a page or fall back its slug if the page is missing
    p = lambda slug: pages.get(slug) or slug

    # Return template context with our menu structure
    return dict(
        pages_top=[
            p('patient'),
            p('exam'),
            p('sale'),
            p('salescomparison'),
        ],
        pages_records=[
            p('patientrecords'),
            p('examrecords'),
            p('salesrecords'),
        ],
        pages_inventory=[
            p('frameinventory'),
            p('lensinventory'),
        ],
        pages_inventory_new=[
            p('newinventory'),
        ],
        pages_products=[
            p('products'),
            p('newproduct'),
        ],
        pages_review=[
            p('inventoryreviewform'),
            p('discrepancyrecords'),
        ],
    )


def active_store(request):
    """
    Returns context with active store, if any, based on URL parameters.
    """
    store_id = request.resolver_match.kwargs.get('store_id')

    if not store_id:
        return dict()

    try:
        active_store = Store.objects.get(pk=store_id)
    except Store.DoesNotExist:
        return dict()

    return dict(
        active_store=active_store,
    )


def active_page(request):
    """
    Returns context with active page, if any, based on URL parameters.
    """
    page_slug = request.resolver_match.kwargs.get('page_slug')

    if not page_slug:
        return dict()

    try:
        active_page = Page.objects.get(slug=page_slug)
    except Page.DoesNotExist:
        return dict()

    return dict(
        active_page=active_page,
    )
