# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-04 09:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("contacts", "0001_initial"), ("deals", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="deal",
            name="contact",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="contacts.Person",
                verbose_name="contact",
            ),
        ),
        migrations.AddField(
            model_name="deal",
            name="customer",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="contacts.Organization",
                verbose_name="customer",
            ),
            preserve_default=False,
        ),
    ]