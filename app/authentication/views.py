from django.shortcuts import render
import magic
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated


class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
