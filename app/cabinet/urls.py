from rest_framework import routers

from app.cabinet.views import CabinetViewSet

router = routers.DefaultRouter()
router.register('v1/cabinet', CabinetViewSet)

urlpatterns = []

app_name = 'cabinet'
urlpatterns += router.urls
