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
        permission_classes=(AllowAny,),
        serializer_class=CreateCoreUserSerializer
    )
    def register(self, request):
        CLIENT_ID = '<r3lLSKSJC0aAKQJzTD8u5ecYgEuU9ghYqEcyquw2>'
        CLIENT_SECRET = '<JVg88AK9uvvpJgGBqpRwSN9OOB7XoiqEawoG24RXOe1H3NHSjOnBFdjBEeVy28Mt5lVV6W1AhM3mFFUKRYz1B4NC7oGxO7EHAWwhKDyrCZYKorBQvx67kZblsd19wjJ6>'
        ser = self.serializer_class(data=request.data)
        if ser.is_valid():
            ser.save()
            host = request.META['HTTP_HOST']
            r = requests.post('http://{}/api/v1/auth/token/'.format(host),
                              data={
                                  'grant_type': 'password',
                                  'username': request.data.get('email'),
                                  'password': request.data.get('password'),
                                  'client_id': CLIENT_ID,
                                  'client_secret': CLIENT_SECRET
                              }
                              )
            return Response(r)
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
