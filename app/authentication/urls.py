from django.urls import path, include
from rest_framework import routers

from app.authentication.views import AuthViewSet

router = routers.DefaultRouter()
router.register('v1/auth', AuthViewSet)

urlpatterns = []

app_name = 'authentication'
urlpatterns += router.urls
urlpatterns += [
    path('v1/auth/', include('rest_framework_social_oauth2.urls')),
]
