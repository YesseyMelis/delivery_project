from rest_framework import routers
from django.conf.urls import url, include

from app.authentication.views import AuthViewSet

router = routers.DefaultRouter()
router.register('v1', AuthViewSet)

urlpatterns = []

app_name = 'authentication'
urlpatterns += router.urls
