# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-02-26 19:55
from __future__ import unicode_literals

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("offers", "0009_auto_20160924_2201")]

    operations = [
        migrations.AddField(
            model_name="offer",
            name="_code",
            field=models.IntegerField(default=0, verbose_name="code"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="offer",
            name="tax_rate",
            field=models.DecimalField(
                decimal_places=2,
                default=Decimal("7.7"),
                max_digits=10,
                verbose_name="tax rate",
            ),
        ),
    ]