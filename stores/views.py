# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django import http
from . import models


log = logging.getLogger('django.stores.views')


def require_store_manager(view_func):
    """
    Provides to decorateed view access to user’s managed stores
    and currently active store.

    If user is not a manager on any stores, returns an HTTP Forbidden
    response.

    Requires user to be logged in (use after ``login_required`` decorator).

    Sets following keyword arguments for the view:

    - ``managed_stores``: a list of managed stores
    - ``active_store``:  store or first store
    """

    def wrapper(request, *args, **kwargs):
        managed_stores = (
            models.get_managed_stores(request.user).order_by('name'))

        if len(managed_stores) < 1:
            log.warning("User not a manager: %s", request.user.username)
            return http.HttpResponseForbidden("User not a manager")

        active_store = (
            _get_selected_store(request) or
            _get_last_selected_store(request) or
            managed_stores[0])

        _set_last_selected_store(request, active_store)

        kwargs['managed_stores'] = managed_stores
        kwargs['active_store'] = active_store

        return view_func(request, *args, **kwargs)

    return wrapper


LAST_VIEWED_STORE_ID_SESSION_KEY = 'last_viewed_store_id'


def _get_selected_store(request):
    """
    Get currently viewed store.
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
        return store if models.is_manager(request.user, store) else None


def _get_last_selected_store(request):
    """
    Get latest selected store.
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
        return store if models.is_manager(request.user, store) else None


def _set_last_selected_store(request, store):
    """
    Saves the ID of given store as latest selected store in user session.
    """
    if store:
        request.session[LAST_VIEWED_STORE_ID_SESSION_KEY] = store.pk
    else:
        if LAST_VIEWED_STORE_ID_SESSION_KEY in request.session:
            del request.session[LAST_VIEWED_STORE_ID_SESSION_KEY]
