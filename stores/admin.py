# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from . import models


class StorePageInline(admin.TabularInline):
    model = models.StorePage


class RegionAdmin(admin.ModelAdmin):
    pass


class StoreAdmin(admin.ModelAdmin):
    inlines = [
        StorePageInline,
    ]


admin.site.register(models.Region, RegionAdmin)
admin.site.register(models.Store, StoreAdmin)
