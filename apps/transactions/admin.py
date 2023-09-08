from django.contrib import admin
from apps.transactions.models import Account, Transaction
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

# Register your models here.


class AccountAdmin(admin.ModelAdmin):
    search_fields = ["user__username", "title"]
    list_display = ["id", "user", "title"]
    actions = ['print_selected_objects']

    def print_selected_objects(self, request, queryset):
        template = loader.get_template('admin/print_selected_objects.html')
        context = {'objects': queryset}
        rendered_template = template.render(context, request)
        response = HttpResponse(rendered_template, content_type='text/html')
        response['Content-Disposition'] = 'attachment; filename="print_selected_objects.html"'
        return response


class TransactionAdmin(admin.ModelAdmin):
    search_fields = [
        "entry_no",
        "from_account",
        "to_account",
        "initial_amount",
        "converted_amount",
        "date",
    ]
    list_display = [
        "entry_no",
        "from_account",
        "to_account",
        "initial_amount",
        "converted_amount",
        "date",
    ]


admin.site.register(Account, AccountAdmin)
admin.site.register(Transaction, TransactionAdmin)




