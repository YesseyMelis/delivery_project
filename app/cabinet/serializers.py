from rest_framework import serializers

from app.cabinet.models import Address, Basket, BasketSubscription
from app.service.models import Meal
from app.service.serializers import MealRetrieveSerializer


class SetUserLocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address


class BasketInfoRetrieveSerializer(serializers.ModelSerializer):
    meals = serializers.SerializerMethodField()

    class Meta:
        model = Basket
        fields = (
            'meals',
        )

    def get_meals(self, obj):
        meals_id = BasketSubscription.objects.filter(basket=obj).values_list('meal', flat=True)
        basket_meals = Meal.objects.filter(id__in=meals_id)
        ser = MealRetrieveSerializer(basket_meals, many=True)
        return ser.data
