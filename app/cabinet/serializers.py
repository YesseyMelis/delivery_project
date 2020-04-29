from rest_framework import serializers

from app.cabinet.models import Address


class SetUserLocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address