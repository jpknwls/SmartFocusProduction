# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.exceptions import ValidationError


class Page(models.Model):
    """Page with iframe-based view(s) into Zoho."""

    level = models.CharField(
        default='CHAIN_LEVEL',
        max_length=20,
        choices=(
            ('CHAIN_LEVEL', 'Chain-level'),
            ('STORE_LEVEL', 'Store-level'),
        ))

    title = models.CharField(
        max_length=255,
        unique=True,
        help_text=
            "Title shown to the user. Example: <tt>入库</tt>")

    description = models.TextField(
        default="",
        blank=True,
        help_text=
            "Optional. Short description to show the user where appropriate.")

    slug = models.SlugField(
        unique=True,
        help_text=
            "Short English identifier. "
            "Used in URLs and to show appropriate icon.<br>"
            "Example: <tt>newinventory</tt>")

    iframe_urls = models.TextField(
        "iframe URLs",
        default="",
        blank=True,
        help_text=
            "One URL per line, no spaces.<br>"
            "NOTE: If this page is store-level, leave this field empty. "
            "Instead, assign store-specific URLs.")

    def __unicode__(self):
        return self.title

    @property
    def icon_path(self):
        return 'images/pages/{0}.png'.format(self.slug)

    def clean(self):
        # TODO
        valid_template = False

        iframe_urls = [u.strip() for u in self.iframe_urls.split('\n')]
        self.iframe_urls = '\n'.join(iframe_urls)

        if self.level == 'CHAIN_LEVEL':
            if self.iframe_urls == '' and valid_template == False:
                raise ValidationError(
                    "You’re creating a chain-level page. "
                    "Make sure you specify either at least one iframe URL "
                    "(if more than one URL then each on its own line), "
                    "or exactly one template filename. ")
