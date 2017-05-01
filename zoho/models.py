# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.db import models
from django.core import exceptions
from django.core import validators
from django import template


CUSTOM_PAGE_TEMPLATE_ROOT = 'pages/'
"""
For pages which specify custom template, they’ll be found under this path.
Relative to template root specified in Django settings.
"""


class Page(models.Model):
    """Page with iframe-based view(s) into Zoho."""

    level = models.CharField(
        default='CHAIN_LEVEL',
        max_length=20,
        choices=(
            ('CHAIN_LEVEL', 'Chain-level'),
            ('STORE_LEVEL', 'Store-level'),
        ),
        help_text=
            "Whether this page’s contents will be different for each store.")

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
        "chain-level page contents",
        default="",
        blank=True,
        help_text=
            "For a chain-level page this field must contain either: "
            "<ol>"
            "<li>At least one iframe URL, if multiple then one per line"
            "<li>One template filename, relative to <tt>templates/pages/</tt>"
            "</ol>"
            "NOTE: if this page is store-level, leave this field empty. "
            "Instead, assign contents in admin sections "
            "corresponding to individual stores.")

    def __unicode__(self):
        return self.title

    @property
    def icon_path(self):
        return 'images/pages/{0}.png'.format(self.slug)

    def clean(self):
        # Prepare chain-wide page contents for validation:
        # strip any trailing white space
        self.iframe_urls = self.iframe_urls.strip()

        if self.level == 'STORE_LEVEL':
            self.clean_store_level()
        elif self.level == 'CHAIN_LEVEL':
            self.clean_chain_level()

    def clean_store_level(self):
        """
        Checks that page’s contents are appropriate to store level,
        which means it should have no chain-wide contents specified.
        """
        if self.iframe_urls != '':
            raise exceptions.ValidationError({
                'iframe_urls':
                    "You’ve chosen to create a store-level page. "
                    "Please specify page contents in sections "
                    "corresponding to individual stores "
                    "and leave chain-level contents empty."
            })

    def clean_chain_level(self):
        """
        Checks that page’s contents are appropriate to chain level.

        * No store-specific contents should be defined
        * Chain-wide contents must not be empty
        * Chain-wide contents must either be a template name or a list of
          valid URLs
        """
        general_errors = []
        content_field_errors = []

        if self.store_pages.count() > 0:
            # Apparently, this page has been created as a chain-level but then
            # converted to store-level. Store-level contents are not allowed.
            general_errors.append(
                "You’re converting a store-level page to chain-level page, "
                "but it still has some store-specific contents assigned. "
                "You can’t set store-specific contents for a chain-level page—"
                "make sure to delete store-level configuration first.")

        if self.iframe_urls == '':
            content_field_errors.append(
                "You’ve chosen to create a chain-level page. "
                "Make sure you specify either at least one iframe URL "
                "(if more than one URL then each on its own line), "
                "or exactly one template filename. ")

        # Let’s see if we are given a template path first
        try:
            tentative_template_path = os.path.join(
                CUSTOM_PAGE_TEMPLATE_ROOT,
                self.iframe_urls)
            template.loader.get_template(tentative_template_path)
        except template.loader.TemplateDoesNotExist:
            valid_template = False
        else:
            valid_template = True

        # If not a template, treat contents as a list of iframe URLs
        if not valid_template:

            iframe_urls = [u.strip() for u in self.iframe_urls.split('\n')]

            for url in iframe_urls:
                try:
                    validators.URLValidator()(url)
                except exceptions.ValidationError, e:
                    content_field_errors.append("{0}: {1}".format(
                        url,
                        ', '.join(e.messages)))

            self.iframe_urls = '\n'.join(iframe_urls)

        if len(general_errors + content_field_errors) > 0:
            raise exceptions.ValidationError({
                exceptions.NON_FIELD_ERRORS: general_errors,
                'iframe_urls': content_field_errors,
            })
