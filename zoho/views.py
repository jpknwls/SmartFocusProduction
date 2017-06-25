# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django.core import exceptions

from . import models


log = logging.getLogger('django.zoho.views')


def require_page_visibility(view_func):
    """
    Provides to decorated view access to user’s visible pages
    and currently active page.

    Passes following keyword arguments to the view:

    - ``visible_pages``: iterable of pages visible to the user
    - ``active_page``: currently selected page or None
    """

    def wrapper(request, *args, **kwargs):
        visible_pages = models.get_visible_pages(request.user)

        if len(visible_pages) < 1:
            log.warning("No pages visible to UID %s", request.user.username)
            raise exceptions.PermissionDenied()

        active_page = _get_selected_page(request, visible_pages)

        kwargs['visible_pages'] = visible_pages
        kwargs['active_page'] = active_page

        return view_func(request, *args, **kwargs)

    return wrapper


def _get_selected_page(request, visible_pages):
    """
    Get currently viewed store among associated stores.

    Returns :class:`stores.models.Store` instance or None.

    Uses named argument in resolved URL pattern.
    """
    page_slug = request.resolver_match.kwargs.get('page_slug')

    if not page_slug:
        return None

    try:
        page = models.Page.objects.get(slug=page_slug)
    except models.Page.DoesNotExist:
        return None
    else:
        return page if page in visible_pages else None
