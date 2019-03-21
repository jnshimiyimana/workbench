# Generated by Django 2.1.7 on 2019-03-21 13:45

from django.db import migrations
from workbench.tools import search


class Migration(migrations.Migration):

    dependencies = [("contacts", "0005_auto_20190321_1025")]

    operations = [
        migrations.RunSQL(search.drop_old_shit("contacts_organization")),
        migrations.RunSQL(search.drop_old_shit("contacts_person")),
        migrations.RunSQL(search.create_structure("contacts_organization")),
        migrations.RunSQL(search.create_structure("contacts_person")),
        migrations.RunSQL(search.fts("contacts_organization", ["name"])),
        migrations.RunSQL(
            search.fts(
                "contacts_person", ["given_name", "family_name", "address", "notes"]
            )
        ),
    ]
