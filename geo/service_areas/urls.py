from rest_framework import routers

from .views import ServiceAreaViewSet

router = routers.SimpleRouter()
router.register('', ServiceAreaViewSet)

urlpatterns = router.urls
