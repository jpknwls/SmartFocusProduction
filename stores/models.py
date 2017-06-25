# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.core import validators
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted_user')[0]


def get_sentinel_group():
    return Group.objects.get_or_create(name='deleted_group')[0]


def get_store_managers_group():
    return Group.objects.get_or_create(name='store managers')[0]


class Region(models.Model):
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='managed_regions',
        on_delete=models.SET(get_sentinel_user),
        help_text=
            "Designates one user as region manager "
            "having access to all pages of all stores "
            "in the region.")

    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class Store(models.Model):
    region = models.ForeignKey('stores.Region')

    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET(get_sentinel_user),
        help_text=
            "Designates one user as store manager "
            "having access to all store pages. ")

    name = models.CharField("localized store name", max_length=255)

    def __unicode__(self):
        return self.name


class StoreAssociate(models.Model):
    store = models.ForeignKey(
        'stores.Store',
        related_name='associates')

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='associated_stores',
        on_delete=models.SET(get_sentinel_user))

    def __unicode__(self):
        return "{0.user} at {0.store}".format(self)


class StorePage(models.Model):
    store = models.ForeignKey(
        'stores.Store',
        related_name='store_pages')

    page = models.ForeignKey(
        'zoho.Page',
        limit_choices_to={'level': 'STORE_LEVEL'},
        related_name='store_pages')

    iframe_urls = models.TextField(
        "store-level iframe URLs",
        help_text=
            "At least one store-specific iframe URL, "
            "if multiple then each on its own line.")

    class Meta:
        verbose_name_plural = "store page contents"
        unique_together = ('page', 'store')

    def __unicode__(self):
        return "{page} for {store}".format(
            page=unicode(self.page),
            store=unicode(self.store))

    def clean(self):
        if self.page.level == 'CHAIN_LEVEL':
            raise ValidationError(
                "Can’t set store-specific contents for a chain-level page!")

        # Validate provided URLs
        iframe_urls = [u.strip() for u in self.iframe_urls.split('\n')]

        errors = []

        for url in iframe_urls:
            try:
                validators.URLValidator()(url)
            except ValidationError, err:
                errors.append("{0}: {1}".format(url, ', '.join(err.messages)))

        self.iframe_urls = '\n'.join(iframe_urls)

        if len(errors) > 0:
            raise ValidationError({'iframe_urls': errors})


def get_associated_stores(user):
    return Store.objects.filter(
        Q(region__manager=user) | Q(manager=user) | Q(associates__user=user))
