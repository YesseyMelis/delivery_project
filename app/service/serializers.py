from rest_framework import serializers

from app.service.models import Restaurant, Menu, MenuSubscription, Meal


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