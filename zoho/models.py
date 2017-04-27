# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Page(models.Model):
    """Page with an iframe view into a Zoho table."""

    iframe_url = models.URLField(
        null=True,
        blank=True,
        help_text=
            "If page is store-specific, leave iframe URL empty here. "
            "You’ll be able to assign this page to the store "
            "and add iframe URL on store edit page.")

    priority = models.PositiveIntegerField(
        default=1,
        help_text="Pages with higher priority appear first in lists.")

    title = models.CharField(
        max_length=255,
        help_text="For example, <tt>View inventory</tt>.")

    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['priority']

    def __unicode__(self):
        return self.title


def get_chain_wide_pages():
    return Page.objects.filter(**CHAIN_WIDE_PAGES_QUERY)


def get_store_specific_pages():
    return Page.objects.filter(**STORE_SPECIFIC_PAGES_QUERY)


STORE_SPECIFIC_PAGES_QUERY = dict(iframe_url__isnull=True)
CHAIN_WIDE_PAGES_QUERY = dict(iframe_url__isnull=False)
