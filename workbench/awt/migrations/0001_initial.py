# Generated by Django 2.1.7 on 2019-02-28 18:37

import datetime
from decimal import Decimal
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]

    operations = [
        migrations.CreateModel(
            name="Absence",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("starts_on", models.DateField(verbose_name="starts on")),
                (
                    "days",
                    models.DecimalField(
                        decimal_places=2, max_digits=4, verbose_name="days"
                    ),
                ),
                ("description", models.TextField(verbose_name="description")),
                (
                    "is_vacation",
                    models.BooleanField(default=True, verbose_name="is vacation"),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="absences",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="user",
                    ),
                ),
            ],
            options={
                "verbose_name": "absence",
                "verbose_name_plural": "absences",
                "ordering": ["-starts_on", "-pk"],
            },
        ),
        migrations.CreateModel(
            name="Employment",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "date_from",
                    models.DateField(
                        default=datetime.date.today, verbose_name="date from"
                    ),
                ),
                (
                    "date_until",
                    models.DateField(
                        default=datetime.date(9999, 12, 31), verbose_name="date until"
                    ),
                ),
                ("percentage", models.IntegerField(verbose_name="percentage")),
                (
                    "vacation_days",
                    models.DecimalField(
                        decimal_places=2,
                        help_text="Vacation days if percentage was active for a full year.",
                        max_digits=4,
                        verbose_name="vacation days",
                    ),
                ),
                ("notes", models.TextField(blank=True, verbose_name="notes")),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="employments",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="user",
                    ),
                ),
            ],
            options={
                "verbose_name": "employment",
                "verbose_name_plural": "employments",
                "ordering": ["date_from"],
            },
        ),
        migrations.CreateModel(
            name="Year",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("year", models.IntegerField(unique=True, verbose_name="year")),
                (
                    "january",
                    models.DecimalField(
                        decimal_places=2, max_digits=4, verbose_name="january"
                    ),
                ),
                (
                    "february",
                    models.DecimalField(
                        decimal_places=2, max_digits=4, verbose_name="february"
                    ),
                ),
                (
                    "march",
                    models.DecimalField(
                        decimal_places=2, max_digits=4, verbose_name="march"
                    ),
                ),
                (
                    "april",
                    models.DecimalField(
                        decimal_places=2, max_digits=4, verbose_name="april"
                    ),
                ),
                (
                    "may",
                    models.DecimalField(
                        decimal_places=2, max_digits=4, verbose_name="may"
                    ),
                ),
                (
                    "june",
                    models.DecimalField(
                        decimal_places=2, max_digits=4, verbose_name="june"
                    ),
                ),
                (
                    "july",
                    models.DecimalField(
                        decimal_places=2, max_digits=4, verbose_name="july"
                    ),
                ),
                (
                    "august",
                    models.DecimalField(
                        decimal_places=2, max_digits=4, verbose_name="august"
                    ),
                ),
                (
                    "september",
                    models.DecimalField(
                        decimal_places=2, max_digits=4, verbose_name="september"
                    ),
                ),
                (
                    "october",
                    models.DecimalField(
                        decimal_places=2, max_digits=4, verbose_name="october"
                    ),
                ),
                (
                    "november",
                    models.DecimalField(
                        decimal_places=2, max_digits=4, verbose_name="november"
                    ),
                ),
                (
                    "december",
                    models.DecimalField(
                        decimal_places=2, max_digits=4, verbose_name="december"
                    ),
                ),
                (
                    "working_time_per_day",
                    models.DecimalField(
                        decimal_places=1,
                        max_digits=4,
                        validators=[
                            django.core.validators.MinValueValidator(Decimal("0.1"))
                        ],
                        verbose_name="working time per day",
                    ),
                ),
            ],
            options={
                "verbose_name": "year",
                "verbose_name_plural": "years",
                "ordering": ["-year"],
            },
        ),
        migrations.AlterUniqueTogether(
            name="employment", unique_together={("user", "date_from")}
        ),
        migrations.RunSQL(
            "SELECT audit_audit_table('awt_year');"
            "SELECT audit_audit_table('awt_employment');"
            "SELECT audit_audit_table('awt_absence');"
        ),
    ]