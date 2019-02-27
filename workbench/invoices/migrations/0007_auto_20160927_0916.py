# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-27 07:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("invoices", "0006_invoice_liable_to_vat")]

    operations = [
        migrations.AlterField(
            model_name="invoice",
            name="type",
            field=models.CharField(
                choices=[
                    ("fixed", "Fixed amount"),
                    ("down-payment", "Down payment"),
                    ("services", "Services"),
                ],
                max_length=20,
                verbose_name="type",
            ),
        )
    ]