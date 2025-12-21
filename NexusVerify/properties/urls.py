from rest_framework.routers import DefaultRouter
from .views import PropertyViewSet
from rest_framework.routers import DefaultRouter
from .views import PropertyViewSet, PropertyAuditViewSet

router = DefaultRouter()
router.register("properties", PropertyViewSet)
router.register("properties-audit", PropertyAuditViewSet, basename="property-audit")

urlpatterns = router.urls



router = DefaultRouter()
router.register("properties", PropertyViewSet)

urlpatterns = router.urls
