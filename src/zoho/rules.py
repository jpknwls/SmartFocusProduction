# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
from __future__ import unicode_literals
from __future__ import absolute_import

import rules


@rules.predicate
def has_page_access(user, page):
    return len(page.groups_visible_to.intersection(user.groups.all())) > 0

rules.add_perm('zoho.access_page', rules.is_staff | has_page_access)
