# Generated by Django 2.1.7 on 2019-03-04 21:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [("activities", "0001_initial"), ("projects", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="activity",
            name="project",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="activities",
                to="projects.Project",
                verbose_name="project",
            ),
        )
    ]