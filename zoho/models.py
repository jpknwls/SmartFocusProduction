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
            "with specific iframe URL on store edit page.")

    priority = models.PositiveIntegerField(
        default=1,
        help_text="Pages with higher priority appear first in lists.")

    title = models.CharField(
        max_length=255,
        help_text="For example, <tt>View inventory</tt>.")

    slug = models.SlugField(unique=True)

    def __unicode__(self):
        return self.title
