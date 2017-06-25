# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
from __future__ import unicode_literals
from __future__ import absolute_import

import rules

from zoho import rules as zoho


@rules.predicate
def manages_store(user, store):
    return user in [store.manager, store.region.manager]

full_store_access = rules.is_staff | manages_store

@rules.predicate
def is_store_associate(user, store):
    return user in store.associates

@rules.predicate
def has_store_page_access(user, store_page):
    return full_store_access.test(user, store_page.store) or all([
        is_store_associate.test(user, store_page.store),
        zoho.has_page_access.test(user, store_page.page)])

rules.add_perm('stores.access_store_page', has_store_page_access)

rules.add_perm('stores.access_store', full_store_access | is_store_associate)
