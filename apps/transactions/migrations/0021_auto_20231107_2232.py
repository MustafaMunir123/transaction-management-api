# Generated by Django 3.2.6 on 2023-11-07 17:32

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0020_alter_account_full_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='mobile_1',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='mobile_2',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, region=None, unique=True),
        ),
    ]