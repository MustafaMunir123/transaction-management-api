from rest_framework import serializers
from apps.transactions.models import (
    Transaction,
    Account
)
from apps.users.api.v1.serializers import CustomUserSerializer


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

    def create(self, validated_data):
        return Transaction.objects.create(**validated_data)

    def update(self, instance, validated_data):
        transaction = Transaction.objects.filter(id=instance.id).update(**validated_data)
        return transaction


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'title', 'note']

    def create(self, validated_data):
        return Account.objects.create(**validated_data)

    def update(self, instance, validated_data):
        account = Account.objects.filter(id=instance.id).update(**validated_data)
        return account