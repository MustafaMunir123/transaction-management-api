from rest_framework import serializers
from apps.transactions.models import (
    Transaction,
    Account,
    Currency,
    CurrencyOpening
)


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["id", "title", "note"]

    def create(self, validated_data):
        return Account.objects.create(**validated_data)

    def update(self, instance, validated_data):
        account = Account.objects.filter(id=instance.id).update(**validated_data)
        return account


class TransactionSerializer(serializers.ModelSerializer):
    read_only_fields = ('date', 'time',)
    from_account = AccountSerializer(read_only=True)
    to_account = AccountSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = [
            "entry_no",
            "date",
            "multiply_by",
            "divide_by",
            "from_currency",
            "to_currency",
            "initial_amount",
            "converted_amount",
            "narration",
            "is_valid",
            "from_account",
            "to_account",
            "time"
        ]

    def create(self, validated_data):
        return Transaction.objects.create(**validated_data)

    def update(self, instance, validated_data):
        transaction = Transaction.objects.filter(id=instance.id).update(
            **validated_data
        )
        return transaction


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['short']


class CurrencyOpeningSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrencyOpening
        fields = '__all__'

    def create(self, validated_data):
        return CurrencyOpening.objects.create(**validated_data)

    def update(self, instance, validated_data):
        currency_opening = CurrencyOpening.objects.filter(id=instance.id).update(**validated_data)
        return currency_opening

