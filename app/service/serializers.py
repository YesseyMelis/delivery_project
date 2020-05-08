from rest_framework import serializers

from app.authentication.serializers import CoreUserSerializer
from app.cabinet.models import BasketSubscription, Basket
from app.service.models import Restaurant, Menu, MenuSubscription, Meal, Order


class RestaurantRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Restaurant
        fields = '__all__'


class MenuRetrieveQueryParamsSerializer(serializers.Serializer):
    restaurant_id = serializers.IntegerField()


class MealRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = (
            'name',
            'price',
            'description',
            'image',
            'created_at',
            'updated_at'
        )


class MenuMealsRetrieveSerializer(serializers.ModelSerializer):
    meals = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = (
            'name',
            'meals'
        )

    def get_meals(self, obj):
        meals_id = MenuSubscription.objects.filter(menu=obj).values_list('meal_id', flat=True)
        menu_meals = Meal.objects.filter(id__in=meals_id)
        ser = MealRetrieveSerializer(menu_meals, many=True)
        return ser.data


class MealAddQueryParamsSerializer(serializers.Serializer):
    meal_id = serializers.IntegerField()


class OrderConfirmQueryParamsSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()


class OrderUpdateQueryParamsSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    courier = serializers.IntegerField(required=False)
    status = serializers.CharField(required=False)
    cost = serializers.FloatField(required=False)


class OrderBasketInfoRetrieveSerializer(serializers.ModelSerializer):
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


class OrderUpdateSerializer(serializers.ModelSerializer):
    courier = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    basket = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            'status',
            'courier',
            'user',
            'cost',
            'basket',
        )

    def get_courier(self, obj):
        ser = CoreUserSerializer(obj.courier)
        return ser.data

    def get_user(self, obj):
        ser = CoreUserSerializer(obj.user)
        return ser.data

    def get_basket(self, obj):
        ser = OrderBasketInfoRetrieveSerializer(obj.basket)
        return ser.data
