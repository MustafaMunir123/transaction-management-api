# Generated by Django 3.2.5 on 2023-08-14 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0002_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='is_valid',
            field=models.BooleanField(default=True),
        ),
    ]
