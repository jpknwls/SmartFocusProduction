# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import http
from django.shortcuts import get_object_or_404

from . import models


def require_store_manager(view_func):
    """
    Decorator for store-specific views. Handles permission control.

    If current user manages this store, calls decorated view.
    Otherwise returns a Forbidden response.
    """
    def wrapper(request, store_id, *args, **kwargs):
        store = get_object_or_404(models.Store, pk=store_id)

        if models.is_manager(request.user, store):
            return view_func(request, store_id, *args, **kwargs)
        else:
            return http.HttpResponseForbidden("You do not manage this store")

    return wrapper
