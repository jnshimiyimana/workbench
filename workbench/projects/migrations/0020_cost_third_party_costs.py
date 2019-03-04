# Generated by Django 2.1.7 on 2019-03-03 15:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("projects", "0019_auto_20190302_1437")]

    operations = [
        migrations.AddField(
            model_name="cost",
            name="third_party_costs",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                default=None,
                help_text="Total incl. tax for third-party services.",
                max_digits=10,
                null=True,
                validators=[django.core.validators.MinValueValidator(0)],
                verbose_name="third party costs",
            ),
        )
    ]