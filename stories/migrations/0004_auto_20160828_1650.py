# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-28 14:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0003_auto_20160828_1023'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='story',
            options={'ordering': ('status', 'position', 'id'), 'verbose_name': 'story', 'verbose_name_plural': 'stories'},
        ),
        migrations.RemoveField(
            model_name='requiredservice',
            name='estimated_effort',
        ),
    ]
