# Generated by Django 2.1.7 on 2019-03-21 13:48

from django.db import migrations
from workbench.tools import search


class Migration(migrations.Migration):

    dependencies = [("invoices", "0009_auto_20190321_0833")]

    operations = [
        migrations.RunSQL(search.drop_old_shit("invoices_invoice")),
        migrations.RunSQL(search.drop_old_shit("invoices_recurringinvoice")),
        migrations.RunSQL(search.create_structure("invoices_invoice")),
        migrations.RunSQL(search.create_structure("invoices_recurringinvoice")),
        migrations.RunSQL(
            search.fts("invoices_invoice", ["title", "description", "postal_address"])
        ),
        migrations.RunSQL(
            search.fts(
                "invoices_recurringinvoice", ["title", "description", "postal_address"]
            )
        ),
    ]
