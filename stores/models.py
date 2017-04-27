# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Region(models.Model):
    manager = models.ForeignKey('auth.User')
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class Store(models.Model):
    region = models.ForeignKey('stores.Region')
    manager = models.ForeignKey('auth.User')
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

    def __unicode__(self):
        return "{page} for {store}".format(
            page=unicode(self.page),
            store=unicode(self.store))
