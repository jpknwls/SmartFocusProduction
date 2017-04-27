# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from . import models
from zoho.models import get_store_specific_pages


class StorePageInline(admin.TabularInline):
    model = models.StorePage


class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'manager', )


class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'has_all_pages_configured', )

    list_filter = ('region', )

    inlines = [
        StorePageInline,
    ]

    def has_all_pages_configured(self, obj):
        return len(obj.store_pages.all()) == len(get_store_specific_pages())
    has_all_pages_configured.short_description = "Has all pages configured?"
    has_all_pages_configured.boolean = True


admin.site.register(models.Region, RegionAdmin)
admin.site.register(models.Store, StoreAdmin)
