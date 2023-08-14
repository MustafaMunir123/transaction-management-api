from django.contrib import admin
from apps.transactions.models import (
    Account,
    Transaction
)

# Register your models here.

class AccountAdmin(admin.ModelAdmin):
    search_fields = ['user__username', 'title']
    list_display = ['user', 'title']


class TransactionAdmin(admin.ModelAdmin):
    search_fields = ['entry_no', 'from_account', 'to_account', 'initial_amount', 'converted_amount', 'date']
    list_display = ['entry_no', 'from_account', 'to_account', 'initial_amount', 'converted_amount', 'date']

admin.site.register(Account, AccountAdmin)
admin.site.register(Transaction, TransactionAdmin)