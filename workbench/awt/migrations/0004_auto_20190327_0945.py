# Generated by Django 2.2rc1 on 2019-03-27 08:45

from django.db import migrations

from workbench.tools import search


class Migration(migrations.Migration):

    dependencies = [("awt", "0003_auto_20190312_1254")]

    operations = [
        migrations.RunSQL(search.create_structure("awt_absence")),
        migrations.RunSQL(search.fts("awt_absence", ["description"])),
        migrations.RunSQL("UPDATE awt_absence SET id=id"),
    ]