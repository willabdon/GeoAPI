from rest_framework import routers

from .views import ProviderViewSet

router = routers.SimpleRouter()
router.register('', ProviderViewSet)

urlpatterns = router.urls
