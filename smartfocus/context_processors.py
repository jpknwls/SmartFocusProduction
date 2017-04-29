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
    chain_pages = Page.objects.filter(level='CHAIN_LEVEL')
    store_pages = Page.objects.filter(level='STORE_LEVEL')

    pages = {}
    for p in list(chain_pages) + list(store_pages):
        pages[p.slug] = p

    return dict(
        pages_top=[
            pages['patient'],
            pages['exam'],
            pages['sale'],
            pages['salescomparison'],
        ],
        pages_records=[
            pages['patientrecords'],
            pages['examrecords'],
            pages['salesrecords'],
        ],
        pages_inventory=[
            pages['frameinventory'],
            pages['lensinventory'],
        ],
        pages_inventory_new=[
            pages['newinventory'],
        ],
        pages_products=[
            pages['products'],
            pages['newproduct'],
        ],
        pages_review=[
            pages['inventoryreviewform'],
            pages['discrepancyrecords'],
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
