import requests
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from app.authentication.models import CoreUser
from app.authentication.serializers import CoreUserSerializer, CreateCoreUserSerializer


class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = (AllowAny,)
    queryset = CoreUser.objects.all()
    serializer_class = CoreUserSerializer

    @action(
        methods=['post'],
        detail=False,
        serializer_class=CreateCoreUserSerializer
    )
    def register(self, request):
        ser = self.serializer_class(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response({'data': 'You are successfully registered'}, status=status.HTTP_200_OK)
        return Response(ser.errors)

    @action(
        methods=['get'],
        detail=False
    )
    def user(self, request):
        user = request.user
        if user is not None:
            ser = self.serializer_class(user)
            return Response({'data': ser.data}, status=status.HTTP_200_OK)
        return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
