# Generated by Django 2.2rc1 on 2019-03-24 17:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("credit_control", "0003_auto_20190321_1447")]

    operations = [
        migrations.CreateModel(
            name="Ledger",
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
                ("name", models.CharField(max_length=100, verbose_name="name")),
            ],
            options={
                "verbose_name": "ledger",
                "verbose_name_plural": "ledgers",
                "ordering": ["name"],
            },
        ),
        migrations.AddField(
            model_name="creditentry",
            name="ledger",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="transactions",
                to="credit_control.Ledger",
                verbose_name="ledger",
            ),
        ),
        migrations.RunSQL(
            "INSERT INTO credit_control_ledger (name) VALUES ('default');"
            "UPDATE credit_control_creditentry SET ledger_id=L.id"
            " FROM credit_control_ledger L;"
        ),
    ]