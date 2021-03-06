# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-29 12:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(choices=[('CHAIN_LEVEL', 'Chain-level'), ('STORE_LEVEL', 'Store-level')], default='CHAIN_LEVEL', max_length=20)),
                ('title', models.CharField(help_text='Title shown to the user. Example: <tt>\u5165\u5e93</tt>', max_length=255, unique=True)),
                ('description', models.TextField(default='', help_text='Optional. Short description to show the user where appropriate.')),
                ('slug', models.SlugField(help_text='Short English identifier. Used in URLs and to show appropriate icon.<br>Example: <tt>newinventory</tt>', unique=True)),
                ('iframe_urls', models.TextField(default='', help_text='One URL per line, no spaces.<br>NOTE: If this page is store-level, leave URLs empty. Use <b>Store Edit</b> page to add this page to stores and provide store-specific URLs.')),
            ],
        ),
    ]
