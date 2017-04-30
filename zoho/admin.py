# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from stores.models import StorePage
from . import models


class StorePageInline(admin.TabularInline):
    model = StorePage


class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', )

    fields = ('level', ('title', 'slug'), 'description', 'iframe_urls', )

    prepopulated_fields = {'slug': ('title', )}

    inlines = [
        StorePageInline,
    ]


admin.site.register(models.Page, PageAdmin)
