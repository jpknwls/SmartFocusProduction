# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from zoho.models import Page


DROPDOWNS = {
    'records': [
        'patientrecords',
        'examrecords',
        'salesrecords',
    ],
    'stock': [
        'frameinventory',
        'lensinventory',
        'newinventory',
        'products',
        'newproduct',
        'inventoryreviewform',
        'discrepancyrecords',
    ],
    'welcome': [
        'documents',
        'about',
    ],
}
"""
Associates a dropdown identifier with a set of page identifiers.
Used in templates to determine which dropdown toggle to highlight.
This needs to be maintained in accordance with navigation used in template.
"""


def active_dropdown(request):
    """
    Helper letting templates know which dropdown toggle
    does currently active page belong to, if any.

    Added context variables: ``active_dropdown``, string.
    """
    if not request.user.is_authenticated():
        return {}

    active_page_slug = request.resolver_match.kwargs.get('page_slug')

    try:
        return dict(
            active_dropdown=[d_name for d_name, d_pages in DROPDOWNS.items()
                             if active_page_slug in d_pages][0],
        )
    except IndexError:
        return {}


def pages(request):
    """
    Added context variables: ``pages``, contains a structure like
    {page_identifier: page, page_identifier_2: page2, ...}.
    """
    if not request.user.is_authenticated():
        return {}

    pages = {}
    for p in Page.objects.all():
        pages[p.slug] = dict(
            pk=p.pk,
            slug=p.slug,
            icon_path=p.icon_path,
            title=p.title,
            description=p.description,
            level=p.level,
        )

    return dict(pages=pages)


def active_page(request):
    """
    Returns context with active page, if any, based on URL parameters.
    Added context variables: ``active_page`` pointing to Page object.
    """
    active_page_slug = request.resolver_match.kwargs.get('page_slug')

    if not active_page_slug:
        return {}

    try:
        active_page = Page.objects.get(slug=active_page_slug)
    except Page.DoesNotExist:
        return {}

    return dict(
        active_page=active_page,
    )
