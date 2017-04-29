# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models import Q


class Region(models.Model):
    manager = models.ForeignKey(
        'auth.User',
        help_text=
            "Selected user will manage all stores belonging "
            "to this region.")

    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class Store(models.Model):
    region = models.ForeignKey('stores.Region')

    manager = models.ForeignKey(
        'auth.User',
        help_text=
            "Selected user will manage this store. "
            "Note that manager assigned to store’s region will "
            "have access as well.")

    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class StorePage(models.Model):
    store = models.ForeignKey(
        'stores.Store',
        related_name='store_pages')

    page = models.ForeignKey(
        'zoho.Page',
        limit_choices_to={'level': 'STORE_LEVEL'},
        related_name='store_pages')

    iframe_urls = models.TextField(
        help_text="One store-specific URL per line, no spaces.")

    class Meta:
        unique_together = ('page', 'store')

    def __unicode__(self):
        return "{page} for {store}".format(
            page=unicode(self.page),
            store=unicode(self.store))


def get_managed_stores(user):
    """
    Returns a QuerySet of ``Store`` instances
    according to user’s management role.
    """
    return Store.objects.filter(Q(region__manager=user) | Q(manager=user))


def is_manager(user, store):
    """Returns ``True`` if ``store`` is managed by ``user``."""
    return store.manager == user or store.region.manager == user
