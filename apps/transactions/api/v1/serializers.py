from rest_framework import serializers
from apps.transactions.models import (
    Transaction,
    Account,
    Currency
)


class TransactionSerializer(serializers.ModelSerializer):
    read_only_fields = ('date', 'time',)

    class Meta:
        model = Transaction
        fields = [
            "entry_no",
            "multiply_by",
            "divide_by",
            "from_currency",
            "to_currency",
            "initial_amount",
            "converted_amount",
            "narration",
            "is_valid",
            "date",
            "time"
        ]

    def create(self, validated_data):
        return Transaction.objects.create(**validated_data)

    def update(self, instance, validated_data):
        transaction = Transaction.objects.filter(id=instance.id).update(
            **validated_data
        )
        return transaction


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["id", "title", "note"]

    def create(self, validated_data):
        return Account.objects.create(**validated_data)

    def update(self, instance, validated_data):
        account = Account.objects.filter(id=instance.id).update(**validated_data)
        return account


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['short']




