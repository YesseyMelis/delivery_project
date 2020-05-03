from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny

from app.cabinet.models import Basket, BasketSubscription
from app.service.models import Restaurant
from app.service.serializers import RestaurantRetrieveSerializer, MenuRetrieveQueryParamsSerializer, \
    MenuMealsRetrieveSerializer, MealAddQueryParamsSerializer


class ServiceViewSet(viewsets.GenericViewSet):
    permission_classes = (AllowAny,)
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantRetrieveSerializer

    @action(
        methods=['get'],
        detail=False,
        url_path='restaurants/list',
        url_name='restaurants/list'
    )
    def restaurants(self, request):
        ser = self.get_serializer(self.get_queryset(), many=True)
        return Response({'data': ser.data}, status=status.HTTP_200_OK)

    @action(
        methods=['get'],
        detail=False,
        url_path='restaurant/menu',
        url_name='restaurant/menu',
        serializer_class=MenuMealsRetrieveSerializer,
    )
    def get_menu(self, request):
        ser_params = MenuRetrieveQueryParamsSerializer(data=request.query_params)
        ser_params.is_valid(raise_exception=True)
        restaurant_id = ser_params.validated_data.get('restaurant_id')
        menus = self.get_queryset().filter(id=restaurant_id)
        if menus.exists():
            menu = menus.first().menu
            ser = self.get_serializer(menu)
            return Response({'data': ser.data}, status=status.HTTP_200_OK)
        return Response({'error': 'Restaurant not found'}, status=status.HTTP_404_NOT_FOUND)


    @action(
        methods=['post'],
        detail=False,
        url_path='meal/add',
        url_name='meal/add',
    )
    def add_meal(self, request):
        user = request.user
        ser_params = MealAddQueryParamsSerializer(data=request.query_params)
        ser_params.is_valid(raise_exception=True)
        meal_id = ser_params.validated_data.get('meal_id')
        basket = Basket.objects.get(user=user)
        BasketSubscription.objects.create(
            basket=basket,
            meal_id=meal_id
        )
        return Response({'data': 'Meal successfully added to the basket'}, status=status.HTTP_200_OK)

