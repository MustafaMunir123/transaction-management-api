# Generated by Django 3.2.6 on 2023-11-05 12:52

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0018_auto_20231105_1744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='mobile_1',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None),
        ),
    ]
