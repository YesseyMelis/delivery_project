from django.conf import settings
from rest_framework import serializers

from app.authentication.serializers import CoreUserSerializer
from app.service.models import Restaurant, Menu, Meal, Order


class RestaurantRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'


class MenuRetrieveQueryParamsSerializer(serializers.Serializer):
    restaurant_id = serializers.IntegerField()


class MealRetrieveSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

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

    def get_image(self, obj):
        return settings.BASE_URL + obj.image.url


class MenuMealsRetrieveSerializer(serializers.ModelSerializer):
    meals = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = (
            'name',
            'meals'
        )

    def get_meals(self, obj):
        menu_meals = obj.meals.all()
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


class OrderInfoSerializer(serializers.ModelSerializer):
    courier = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    meals = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            'status',
            'courier',
            'user',
            'cost',
            'meals',
        )

    def get_courier(self, obj):
        ser = CoreUserSerializer(obj.courier)
        return ser.data

    def get_user(self, obj):
        ser = CoreUserSerializer(obj.user)
        return ser.data

    def get_meals(self, obj):
        order_meals = obj.meals.all()
        ser = MealRetrieveSerializer(order_meals, many=True)
        return ser.data
