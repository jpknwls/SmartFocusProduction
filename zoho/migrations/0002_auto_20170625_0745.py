# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-25 07:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
        ('zoho', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='groups_visible_to',
            field=models.ManyToManyField(blank=True, help_text='Designates which groups a user must belong to in order to access this page. (Has no effect on managers. Has no effect at all if access restriction is not enabled.)<br>', related_name='pages_visible', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='page',
            name='is_restricted',
            field=models.BooleanField(default=False, help_text='Designates that the page should only be accessible by select user groups.', verbose_name='enable access restriction'),
        ),
        migrations.AlterField(
            model_name='page',
            name='description',
            field=models.TextField(blank=True, default='', help_text='Optional. Short description to show the user where appropriate.'),
        ),
        migrations.AlterField(
            model_name='page',
            name='iframe_urls',
            field=models.TextField(blank=True, default='', help_text='For a chain-level page this field must contain either: <ol><li>At least one iframe URL, if multiple then one per line<li>One template filename, relative to <tt>templates/pages/</tt></ol>NOTE: if this page is store-level, leave this field empty. Instead, assign contents in admin sections corresponding to individual stores.', verbose_name='chain-level page contents'),
        ),
        migrations.AlterField(
            model_name='page',
            name='level',
            field=models.CharField(choices=[('CHAIN_LEVEL', 'Chain-level'), ('STORE_LEVEL', 'Store-level')], default='CHAIN_LEVEL', help_text='Whether this page\u2019s contents will be different for each store.', max_length=20),
        ),
    ]
