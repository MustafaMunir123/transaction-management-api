from django.db import models
from apps.users.models import CustomUser
from apps.transactions.constants import CURRENCY_CHOICES

# Create your models here.


class CurrencyOpening(models.Model):
    objects = None
    currency = models.CharField(max_length=3, null=False, blank=False)
    account = models.ForeignKey('Account', on_delete=models.CASCADE, related_name='currency_openings')


class Account(models.Model):
    objects = None
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="accounts")
    title = models.CharField(max_length=100, null=False, blank=False, unique=True)
    note = models.TextField(max_length=200, null=True)

    def __str__(self):
        return f"{self.title}  {self.note}"

    class Meta:
        permissions = [
            ("view_yourmodel", "Can view YourModel"),
            ("edit_yourmodel", "Can edit YourModel"),
        ]


class Transaction(models.Model):
    objects = None
    entry_no = models.BigAutoField(primary_key=True, auto_created=True, serialize=False)
    from_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="transactions_from")
    to_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="transactions_to")
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    from_currency = models.CharField(max_length=3, null=False, blank=False, choices=CURRENCY_CHOICES)
    to_currency = models.CharField(max_length=3, null=False, blank=False, choices=CURRENCY_CHOICES)
    initial_amount = models.FloatField(null=False, blank=False)
    converted_amount = models.FloatField(null=False, blank=False)
    multiply_by = models.FloatField(null=False)
    divide_by = models.FloatField(null=False)
    pre_date = models.DateField(auto_now_add=True)
    pre_time = models.TimeField(auto_now_add=True)
    narration = models.TextField(null=False, blank=False, max_length=200)
    is_valid = models.BooleanField(default=True, null=False)

    def __str__(self):
        return f"{self.to_account}  {self.from_account}"


class Currency(models.Model):
    objects = None
    short = models.CharField(max_length=3, null=False, blank=False, help_text="Turn On Capslock")

    class Meta:
        verbose_name_plural = "Currencies"

    def __str__(self):
        return self.short
