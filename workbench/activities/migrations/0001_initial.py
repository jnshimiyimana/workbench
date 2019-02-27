# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-24 07:38
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("contacts", "0001_initial"),
        ("deals", "0001_initial"),
        ("projects", "0001_initial"),
        ("audit", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Activity",
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
                ("title", models.CharField(max_length=200, verbose_name="title")),
                (
                    "due_on",
                    models.DateField(blank=True, null=True, verbose_name="due on"),
                ),
                ("time", models.TimeField(blank=True, null=True, verbose_name="time")),
                (
                    "duration",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        help_text="Duration in hours (if applicable).",
                        max_digits=5,
                        null=True,
                        verbose_name="duration",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="created at"
                    ),
                ),
                (
                    "completed_at",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="completed at"
                    ),
                ),
                (
                    "contact",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="activities",
                        to="contacts.Person",
                        verbose_name="contact",
                    ),
                ),
                (
                    "deal",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="activities",
                        to="deals.Deal",
                        verbose_name="deal",
                    ),
                ),
                (
                    "owned_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="activities",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="owned by",
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="activities",
                        to="projects.Project",
                        verbose_name="project",
                    ),
                ),
            ],
            options={
                "ordering": ("due_on",),
                "verbose_name_plural": "activities",
                "verbose_name": "activity",
            },
        ),
        migrations.RunSQL("SELECT audit_audit_table('activities_activity')", ""),
    ]