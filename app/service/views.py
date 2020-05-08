from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated

from app.cabinet.models import Basket, BasketSubscription
from app.service.models import Restaurant, Order
from app.service.serializers import RestaurantRetrieveSerializer, MenuRetrieveQueryParamsSerializer, \
    MenuMealsRetrieveSerializer, MealAddQueryParamsSerializer, \
    OrderConfirmQueryParamsSerializer, OrderUpdateQueryParamsSerializer, OrderUpdateSerializer


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
        permission_classes=(IsAuthenticated,)
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

    @action(
        methods=['post'],
        detail=False,
        url_path='order/confirm',
        url_name='order/confirm',
        permission_classes=(IsAuthenticated,)
    )
    def confirm_order(self, request):
        user = request.user
        ser_params = OrderConfirmQueryParamsSerializer(data=request.query_params)
        ser_params.is_valid(raise_exception=True)
        order_id = ser_params.validated_data.get('order_id')
        if user.orders.filter(id=order_id).exists():
            order = user.orders.get(id=order_id)
            order.status = Order.CONFIRMED
            order.save()
            return Response({'data': 'The order confirmed!'}, status=status.HTTP_200_OK)
        return Response({'error': 'Order does not exist'}, status=status.HTTP_404_NOT_FOUND)

    @action(
        methods=['post'],
        detail=False,
        url_path='order/create',
        url_name='order/create',
        permission_classes=(IsAuthenticated,)
    )
    def create_order(self, request):
        user = request.user
        basket = Basket.objects.get(user=user)
        Order.objects.create(user=user, basket=basket)
        return Response({'data': 'Order successfully created'}, status=status.HTTP_200_OK)

    @action(
        methods=['post'],
        detail=False,
        url_path='order/update',
        url_name='order/update',
        permission_classes=(IsAuthenticated,)
    )
    def update_order(self, request):
        ser_params = OrderUpdateQueryParamsSerializer(data=request.data)
        ser_params.is_valid(raise_exception=True)
        order_id, courier, order_status, cost = (
            ser_params.validated_data.get('order_id'),
            ser_params.validated_data.get('courier'),
            ser_params.validated_data.get('status'),
            ser_params.validated_data.get('cost')
        )
        data = {
            'courier_id': courier,
            'status': order_status,
            'cost': cost
        }
        order = Order.objects.filter(id=order_id)
        if order.exists():
            order.update(**data)
            ser = OrderUpdateSerializer(order.first())
            return Response({'data': ser.data}, status=status.HTTP_200_OK)
        return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
