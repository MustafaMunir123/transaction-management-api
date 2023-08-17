from django.db import models
from apps.users.models import CustomUser

# Create your models here.

class Account(models.Model):
    objects = None
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='accounts')
    title = models.CharField(max_length=100, null=False, blank=False)
    note = models.TextField(max_length=200, null=True)

    def __str__(self):
        return f"{self.title}  {self.note}"


class Transaction(models.Model):
    objects = None
    entry_no = models.BigAutoField(primary_key=True)
    from_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions_from')
    to_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions_to')
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    from_currency = models.CharField(max_length=3, null=False, blank=False)
    to_currency = models.CharField(max_length=3, null=False, blank=False)
    initial_amount = models.FloatField(null=False, blank=False)
    converted_amount = models.FloatField(null=False, blank=False)
    multiply_by = models.FloatField(null=True)
    divide_by = models.FloatField(null=True)
    pre_date = models.DateField(auto_now_add=True)
    pre_time = models.TimeField(auto_now_add=True)
    narration = models.TextField(null=True, blank=False, max_length=200)
    is_valid = models.BooleanField(default=True, null=False)

    def __str__(self):
        return f"{self.to_account}  {self.from_account}"
