from rest_framework import routers

from app.service.views import ServiceViewSet

router = routers.DefaultRouter()
router.register('v1/service', ServiceViewSet)

urlpatterns = []

app_name = 'service'
urlpatterns += router.urls
