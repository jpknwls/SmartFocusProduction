# -*- coding: utf-8 -*-
# pylint: disable=no-self-use
from __future__ import unicode_literals

from django.contrib import admin

from stores.models import StorePage, Store
from . import models


class StorePageInline(admin.TabularInline):
    model = StorePage


class PageAdmin(admin.ModelAdmin):
    list_display = ('slug', 'title', 'level', 'has_all_stores_configured', )

    fields = ('level', ('title', 'slug'), 'description', 'iframe_urls', )

    prepopulated_fields = {'slug': ('title', )}

    inlines = [
        StorePageInline,
    ]

    def has_all_stores_configured(self, obj):
        if obj.level == 'CHAIN_LEVEL':
            return True
        expected_store_num = len(Store.objects.all())
        return len(obj.store_pages.all()) == expected_store_num
    has_all_stores_configured.short_description = "Has all stores configured?"
    has_all_stores_configured.boolean = True


admin.site.register(models.Page, PageAdmin)
