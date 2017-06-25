# -*- coding: utf-8 -*-
# pylint: disable=no-self-use
from __future__ import unicode_literals

from django import forms
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as StockUserAdmin

from zoho.models import Page

from . import models


class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'manager', )

class StoreAssociateInline(admin.TabularInline):
    model = models.StoreAssociate
    raw_id_fields = ['user']

class StorePageInlineForm(forms.ModelForm):
    class Meta:
        exclude = []
        model = models.StorePage
        widgets = {
            'iframe_urls': forms.Textarea(attrs={
                'rows': 3,
                'style': 'width: 90%'}),
        }

class StorePageInline(admin.TabularInline):
    form = StorePageInlineForm
    model = models.StorePage
    verbose_name_plural = "store-level page contents"

class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'manager', 'has_all_pages_configured',
        'has_any_associates_configured', )

    list_filter = ('region', )

    fields = ('region', 'name', 'manager')

    inlines = [
        StoreAssociateInline,
        StorePageInline,
    ]

    def has_all_pages_configured(self, obj):
        expected_page_num = len(Page.objects.filter(level='STORE_LEVEL'))
        return len(obj.store_pages.all()) == expected_page_num
    has_all_pages_configured.short_description = "Has all pages configured?"
    has_all_pages_configured.boolean = True

    def has_any_associates_configured(self, obj):
        return len(obj.associates.all()) > 0
    has_any_associates_configured.short_description = "Has any associates?"
    has_any_associates_configured.boolean = True

admin.site.register(models.Region, RegionAdmin)
admin.site.register(models.Store, StoreAdmin)


# STOCK USER ADMIN OVERRIDE

def _get_fieldsets():
    _fs = []
    for fieldset in StockUserAdmin.fieldsets:
        if 'groups' not in fieldset[1]['fields']:
            _fs.append(fieldset)
        else:
            fieldset[1]['fields'] = tuple([
                _f for _f in fieldset[1]['fields']
                if _f not in ['user_permissions']
            ])
            _fs.append(fieldset)
    return tuple(_fs)

class UserStoreAssociateInline(admin.TabularInline):
    model = models.StoreAssociate
    verbose_name_plural = "store associations"
    verbose_name = "store associate"

class UserAdmin(StockUserAdmin):
    fieldsets = _get_fieldsets()

    inlines = [
        UserStoreAssociateInline,
    ]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
