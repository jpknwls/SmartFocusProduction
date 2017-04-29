# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from . import models


class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', )

    fields = ('level', ('title', 'slug'), 'description', 'iframe_urls', )

    prepopulated_fields = {'slug': ('title', )}


admin.site.register(models.Page, PageAdmin)
