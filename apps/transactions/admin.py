# Third Party Imports
from django.contrib import admin

# Local Imports
from apps.transactions.models import Account, Currency, CurrencyOpening, Transaction


class AccountAdmin(admin.ModelAdmin):
    search_fields = ["user__username", "title"]
    list_display = ["id", "user", "title"]


class TransactionAdmin(admin.ModelAdmin):
    search_fields = ["entry_no", "from_account", "to_account", "initial_amount", "converted_amount", "date"]
    list_display = ["entry_no", "from_account", "to_account", "initial_amount", "converted_amount", "date"]


class CurrencyAdmin(admin.ModelAdmin):
    search_fields = ["short"]
    list_display = ["short"]


class CurrencyOpeningAdmin(admin.ModelAdmin):
    search_fields = ["currency", "account__id"]
    list_display = ["currency", "account"]


admin.site.register(Account, AccountAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Currency, CurrencyAdmin)
admin.site.register(CurrencyOpening, CurrencyOpeningAdmin)
