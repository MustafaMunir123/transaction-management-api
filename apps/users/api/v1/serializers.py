from rest_framework import serializers
from apps.users.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

    def create(self, validated_data):
        return CustomUser.objects.create(**validated_data)

    def update(self, instance, validated_data):
        custom_user = CustomUser.objects.filter(id=instance.id).update(**validated_data)
        return custom_user