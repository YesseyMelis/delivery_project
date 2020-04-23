from rest_framework import serializers
from app.authentication.models import CoreUser
from app.utils.utils import get_or_none


class CoreUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoreUser
        fields = '__all__'
