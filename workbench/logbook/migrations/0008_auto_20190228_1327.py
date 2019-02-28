# Generated by Django 2.1.7 on 2019-02-28 12:27

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("logbook", "0007_auto_20190226_2249")]

    operations = [
        migrations.AlterField(
            model_name="loggedhours",
            name="hours",
            field=models.DecimalField(
                decimal_places=2,
                max_digits=5,
                validators=[django.core.validators.MinValueValidator(Decimal("0.1"))],
                verbose_name="hours",
            ),
        ),
        migrations.AddIndex(
            model_name="loggedhours",
            index=models.Index(
                fields=["-rendered_on"], name="logbook_log_rendere_ea492e_idx"
            ),
        ),
    ]