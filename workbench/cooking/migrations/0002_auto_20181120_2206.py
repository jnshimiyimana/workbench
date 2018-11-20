# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-20 21:06
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cooking', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Presence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(verbose_name='year')),
                ('percentage', models.IntegerField(verbose_name='percentage')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'presence',
                'verbose_name_plural': 'presences',
                'ordering': ['year'],
            },
        ),
        migrations.AlterModelOptions(
            name='day',
            options={'ordering': ['day'], 'verbose_name': 'day', 'verbose_name_plural': 'days'},
        ),
        migrations.AlterField(
            model_name='day',
            name='handled_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='handled by'),
        ),
    ]
