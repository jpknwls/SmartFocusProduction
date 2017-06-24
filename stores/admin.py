# -*- coding: utf-8 -*-
# pylint: disable=no-self-use
from __future__ import unicode_literals

from django.contrib import admin

from zoho.models import Page

from . import models


class StorePageInline(admin.TabularInline):
    model = models.StorePage


class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'manager', )


class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'manager', 'has_all_pages_configured', )

    list_filter = ('region', )

    inlines = [
        StorePageInline,
    ]

    def has_all_pages_configured(self, obj):
        expected_page_num = len(Page.objects.filter(level='STORE_LEVEL'))
        return len(obj.store_pages.all()) == expected_page_num
    has_all_pages_configured.short_description = "Has all pages configured?"
    has_all_pages_configured.boolean = True


admin.site.register(models.Region, RegionAdmin)
admin.site.register(models.Store, StoreAdmin)
