# Generated by Django 3.1.3 on 2020-11-30 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0011_auto_20201017_1018"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="planning_hours_per_day",
            field=models.DecimalField(
                decimal_places=2,
                default=6,
                help_text="How many hours are available for freely planning projects?",
                max_digits=5,
                verbose_name="planning hours per day",
            ),
        ),
    ]
