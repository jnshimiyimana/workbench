# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-24 11:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("logbook", "0002_loggedcost")]

    operations = [
        migrations.AlterField(
            model_name="loggedcost",
            name="cost",
            field=models.DecimalField(
                decimal_places=2,
                help_text="Total incl. tax for third-party costs.",
                max_digits=10,
                verbose_name="cost",
            ),
        )
    ]