# Third Party Imports
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework.exceptions import ValidationError

# Local Imports
from apps.transactions.constants import CURRENCY_CHOICES
from apps.users.models import CustomUser

# Create your models here.


def validate_decimals(value):
    try:
        return round(float(value), 4)
    except Exception:
        raise ValidationError("Not an integer or a float  number")


class CurrencyOpening(models.Model):
    objects = None
    currency = models.CharField(max_length=3, null=False, blank=False)
    account = models.ForeignKey("Account", on_delete=models.CASCADE, related_name="currency_openings")
    opening = models.FloatField(validators=[validate_decimals], default=0.0000)


class Account(models.Model):
    objects = None
    full_name = models.CharField(max_length=150, null=False, blank=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="accounts")
    title = models.CharField(max_length=100, null=False, blank=False, unique=True)
    note = models.TextField(max_length=200, null=False)
    mobile_1 = PhoneNumberField(null=False, unique=True)
    mobile_2 = PhoneNumberField(null=True, unique=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    company_name = models.CharField(max_length=200, null=True, blank=True)
    authorize = models.BooleanField(default=True, null=False, blank=False)

    def __str__(self):
        return f"{self.title}  {self.note}"

    class Meta:
        permissions = [
            ("view_yourmodel", "Can view YourModel"),
            ("edit_yourmodel", "Can edit YourModel"),
        ]


class Transaction(models.Model):
    objects = None
    entry_no = models.IntegerField(auto_created=False, primary_key=True)
    from_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="transactions_from")
    to_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="transactions_to")
    date = models.DateField(
        auto_now_add=False,
    )
    time = models.TimeField(auto_now_add=True)
    from_currency = models.CharField(max_length=3, null=False, blank=False, choices=CURRENCY_CHOICES)
    to_currency = models.CharField(max_length=3, null=False, blank=False, choices=CURRENCY_CHOICES)
    initial_amount = models.FloatField(null=False, blank=False)
    converted_amount = models.FloatField(null=False, blank=False)
    multiply_by = models.FloatField(null=False)
    divide_by = models.FloatField(null=False)
    narration = models.TextField(null=False, blank=False, max_length=200)
    is_valid = models.BooleanField(default=True, null=False)
    is_archived = models.BooleanField(default=False, null=True)

    def __str__(self):
        return f"{self.to_account}  {self.from_account}"


class Currency(models.Model):
    objects = None
    short = models.CharField(max_length=3, null=False, blank=False, help_text="Turn On Capslock")

    class Meta:
        verbose_name_plural = "Currencies"

    def __str__(self):
        return self.short
