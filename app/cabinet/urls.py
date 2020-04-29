from rest_framework import routers
from django.conf.urls import url, include


router = routers.DefaultRouter()

urlpatterns = []

app_name = 'cabinet'
urlpatterns += router.urls