from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from app.authentication.models import CoreUser
from app.authentication.serializers import CoreUserSerializer


class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = CoreUser.objects.all()
    serializer_class = CoreUserSerializer

    @action(
        methods=['get'],
        detail=False
    )
    def user(self, request):
        user = request.user
        if user:
            ser = self.serializer_class(user)
            return Response({'data': ser.data}, status=status.HTTP_200_OK)
        return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
