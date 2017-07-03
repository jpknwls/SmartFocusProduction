# -*- coding: utf-8 -*-
from __future__ import unicode_literals


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
