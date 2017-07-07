# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django.core import exceptions

from . import models


log = logging.getLogger('django.stores.views')


def require_store_association(view_func):
    """
    Provides to decorateed view access to user’s associated stores
    and currently active store.

    If user is not associated with any stores, returns an HTTP Forbidden
    response.

    Use after ``login_required`` decorator to ensure user is logged in.

    Passes the following keyword arguments to the view:

    - ``associated_stores``: iterable of associated stores
    - ``active_store``:  chosen store or first associated store
    """

    def wrapper(request, *args, **kwargs):
        associated_stores = (
            models.get_associated_stores(request.user).order_by('region'))

        print(associated_stores)
        
        if len(associated_stores) < 1:
            log.warning("No associated stores with UID %s", request.user.username)
            raise exceptions.PermissionDenied()

        active_store = (
            _get_selected_store(request, associated_stores) or
            _get_last_selected_store(request, associated_stores) or
            associated_stores[0])

        _set_last_selected_store(request, active_store)

        kwargs['associated_stores'] = associated_stores
        kwargs['active_store'] = active_store

        return view_func(request, *args, **kwargs)

    return wrapper


LAST_VIEWED_STORE_ID_SESSION_KEY = 'last_viewed_store_id'


def _get_selected_store(request, associated_stores):
    """
    Get currently viewed store among associated stores.

    Returns :class:`stores.models.Store` instance or None.

    Uses named argument in resolved URL pattern.
    """
    store_id = request.resolver_match.kwargs.get('store_id')

    if not store_id:
        return None

    try:
        store = models.Store.objects.get(pk=store_id)
    except models.Store.DoesNotExist:
        return None
    else:
        return store if store in associated_stores else None


def _get_last_selected_store(request, associated_stores):
    """
    Get latest selected store among given associated stores.

    Returns :class:`stores.models.Store` instance or None.

    Checkes user’s session for store ID.
    """
    store_id = request.session.get(LAST_VIEWED_STORE_ID_SESSION_KEY)

    if not store_id:
        return None

    try:
        store = models.Store.objects.get(pk=store_id)
    except models.Store.DoesNotExist:
        return None
    else:
        return store if store in associated_stores else None


def _set_last_selected_store(request, store):
    """
    Saves the ID of given store as latest selected store in user session.
    """
    if store:
        request.session[LAST_VIEWED_STORE_ID_SESSION_KEY] = store.pk
    else:
        if LAST_VIEWED_STORE_ID_SESSION_KEY in request.session:
            del request.session[LAST_VIEWED_STORE_ID_SESSION_KEY]
