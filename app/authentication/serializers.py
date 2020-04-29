from rest_framework import serializers
from app.authentication.models import CoreUser


class CoreUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoreUser
        fields = '__all__'


class CreateCoreUserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = CoreUser.objects.create_user(**validated_data)
        return user

    class Meta:
        model = CoreUser
        fields = ('id', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }