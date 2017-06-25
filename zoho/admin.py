# -*- coding: utf-8 -*-
# pylint: disable=no-self-use
from __future__ import unicode_literals

from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group

from stores.models import StorePage, Store

from . import models


class StorePageInlineForm(forms.ModelForm):
    class Meta:
        exclude = []
        model = StorePage
        widgets = {
            'iframe_urls': forms.Textarea(attrs={
                'rows': 3,
                'style': 'width: 90%'}),
        }

class StorePageInline(admin.TabularInline):
    model = StorePage
    form = StorePageInlineForm
    verbose_name_plural = "page contents: store-level"

class PageForm(forms.ModelForm):
    class Meta:
        exclude = []
        model = models.Page
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2, 'cols': 40}),
            'iframe_urls': forms.Textarea(attrs={
                'rows': 4,
                'style': 'width: 90%'}),
        }

class PageAdmin(admin.ModelAdmin):
    form = PageForm

    list_display = ('slug', 'title', 'level', 'has_all_stores_configured', )

    fieldsets = (
        (None, {'fields': (('level', 'slug'), )}),
        (None, {'fields': (('title', 'description'), )}),
        ("Access control", {
            'description':
                "Designates which user groups this page should be visible to.<br>"
                "If enabled:"
                "<br>—A chain-level page will be accessible by any user "
                "who belongs to at least one of selected groups"
                "<br>—A store-level page will be accessible by store associates "
                "who belong to at least one of selected groups"
                "<br>"
                "No effect on users designated as managers.",
            'classes': ['collapse'],
            'fields': ('is_restricted', 'groups_visible_to', )}),
        ("PAGE CONTENTS: CHAIN-LEVEL", {'fields': ('iframe_urls', )}),
    )

    prepopulated_fields = {'slug': ('title', )}

    filter_horizontal = ['groups_visible_to']

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


# STOCK GROUP ADMIN OVERRIDE

class GroupPageInline(admin.TabularInline):
    model = models.Page.groups_visible_to.through
    readonly_fields = ['page']
    verbose_name_plural = "pages visible to this group"
    extra = 0
    can_delete = False
    max_num = 0

class GroupAdmin(admin.ModelAdmin):
    exclude = ['permissions']

    fieldsets = (
        (None, {
            'description':
                "Separate users into groups "
                "according to their roles. "
                "<br>"
                "Pages visible to this group "
                "can be edited via page edit screens."
                "<br>"
                "Example group names: "
                "<i>clinicians</i>, <i>managers</i>, <i>salespeople</i>, "
                "<i>store managers</i>.",
            'fields': ['name'],
        }),
    )

admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
