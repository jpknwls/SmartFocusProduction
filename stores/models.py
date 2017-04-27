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
        limit_choices_to={'iframe_url__isnull': True})

    iframe_url = models.URLField()

    class Meta:
        unique_together = ('page', 'store')
        ordering = ['page__priority']

    def __unicode__(self):
        return "{page} for {store}".format(
            page=unicode(self.page),
            store=unicode(self.store))


def get_stores_managed_by(user):
    return Store.objects.filter(Q(region__manager=user) | Q(manager=user))
