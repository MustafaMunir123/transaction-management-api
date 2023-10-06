# Generated by Django 3.2.6 on 2023-10-06 12:52

import apps.transactions.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0014_alter_currencyopening_opening'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currencyopening',
            name='opening',
            field=models.FloatField(default=0.0, validators=[apps.transactions.models.validate_decimals]),
        ),
    ]
