# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from . import models


class RegionAdmin(admin.ModelAdmin):
    pass


class StoreAdmin(admin.ModelAdmin):
    pass


class StorePageAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Region, RegionAdmin)
admin.site.register(models.Store, StoreAdmin)
admin.site.register(models.StorePage, StorePageAdmin)
