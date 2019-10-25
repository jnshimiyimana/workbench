# Generated by Django 2.2.5 on 2019-09-16 09:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("offers", "0006_offer_total_excl_tax")]

    operations = [
        migrations.RunSQL(
            "SET SESSION application_name TO 'Migrations';"
            "UPDATE offers_offer SET total_excl_tax=subtotal - discount;"
        )
    ]