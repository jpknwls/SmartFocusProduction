# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.db import models
from django.dispatch import receiver


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
        help_text=
            "Optional. Short description to show the user where appropriate.")

    slug = models.SlugField(
        unique=True,
        help_text=
            "Short English identifier. "
            "Used in URLs and to show appropriate icon.<br>"
            "Example: <tt>newinventory</tt>")

    iframe_urls = models.TextField(
        default="",
        help_text=
            "One URL per line, no spaces.<br>"
            "NOTE: If this page is store-level, leave URLs empty. "
            "Use <b>Store Edit</b> page to add this page to stores "
            "and provide store-specific URLs.")

    def __unicode__(self):
        return self.title

    @property
    def icon_path(self):
        return 'images/{0}.png'.format(self.slug)


# # These two auto-delete icons from filesystem when they are unneeded:
#
# @receiver(models.signals.post_delete, sender=Page)
# def auto_delete_file_on_delete(sender, instance, **kwargs):
#     """
#     Deletes icon from filesystem
#     when corresponding ``Page`` object is deleted.
#     """
#     if instance.file:
#         if os.path.isfile(instance.file.path):
#             os.remove(instance.file.path)
#
# @receiver(models.signals.pre_save, sender=Page)
# def auto_delete_file_on_change(sender, instance, **kwargs):
#     """Deletes icon from filesystem
#     when corresponding ``Page`` object is changed.
#     """
#     if not instance.pk:
#         return False
#
#     try:
#         old_file = Page.objects.get(pk=instance.pk).file
#     except Page.DoesNotExist:
#         return False
#
#     new_file = instance.file
#     if not old_file == new_file:
#         if os.path.isfile(old_file.path):
#             os.remove(old_file.path)
