# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from stores.models import get_stores_managed_by
from zoho.models import get_chain_wide_pages


def managed_stores(request):
    return dict(
        stores=
            get_stores_managed_by(request.user).
            prefetch_related('store_pages'),
    )


def chain_wide_pages(request):
    return dict(
        pages=get_chain_wide_pages(),
    )
