# Generated by Django 3.2.5 on 2023-08-14 16:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("transactions", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Transaction",
            fields=[
                ("entry_no", models.BigAutoField(primary_key=True, serialize=False)),
                ("date", models.DateField(auto_now_add=True)),
                ("time", models.TimeField(auto_now_add=True)),
                ("from_currency", models.CharField(max_length=3)),
                ("to_currency", models.CharField(max_length=3)),
                ("initial_amount", models.FloatField()),
                ("converted_amount", models.FloatField()),
                ("multiply_by", models.FloatField(null=True)),
                ("divide_by", models.FloatField(null=True)),
                ("pre_date", models.DateField(auto_now_add=True)),
                ("pre_time", models.TimeField(auto_now_add=True)),
                ("narration", models.TextField(max_length=200, null=True)),
                (
                    "from_account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="transactions_from",
                        to="transactions.account",
                    ),
                ),
                (
                    "to_account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="transactions_to",
                        to="transactions.account",
                    ),
                ),
            ],
        ),
    ]
