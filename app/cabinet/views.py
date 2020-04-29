from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated

from app.cabinet.models import Address
from app.cabinet.serializers import SetUserLocationSerializer


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
