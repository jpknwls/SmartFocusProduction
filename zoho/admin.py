# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from . import models


class PageAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Page, PageAdmin)
