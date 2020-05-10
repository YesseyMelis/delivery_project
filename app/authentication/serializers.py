from rest_framework import serializers
from app.authentication.models import CoreUser
from app.service.models import Order


class CoreUserSerializer(serializers.ModelSerializer):
    address = serializers.CharField(source='address.name', allow_null=True)

    class Meta:
        model = CoreUser
        fields = (
            'id',
            'email',
            'nickname',
            'phone',
            'first_name',
            'last_name',
            'is_courier',
            'address'
        )


class CreateCoreUserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = CoreUser.objects.create_user(**validated_data)
        Order.objects.create(user=user)
        return user

    class Meta:
        model = CoreUser
        fields = ('id', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }
