from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from app.cabinet.models import Address, Basket
from app.cabinet.serializers import SetUserLocationSerializer, BasketInfoRetrieveSerializer


class CabinetViewSet(viewsets.GenericViewSet):
    permission_classes = (AllowAny,)
    queryset = Address.objects.all()


    @action(
        methods=['post'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        serializer_class=SetUserLocationSerializer
    )
    def set_location(self, request):
        return

    @action(
        methods=['get'],
        detail=False,
        url_path='basket/info',
        url_name='basket/info',
        permission_classes=(IsAuthenticated,)
    )
    def basket_info(self, request):
        user = request.user
        if Basket.objects.filter(user=user):
            basket = Basket.objects.get(user=user)
            ser = BasketInfoRetrieveSerializer(basket)
            return Response({'data': ser.data}, status=status.HTTP_200_OK)
        return Response({'error': 'Basket not exists'}, status=status.HTTP_404_NOT_FOUND)
