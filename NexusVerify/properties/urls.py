from rest_framework.routers import DefaultRouter
from .views import PropertyViewSet, PropertyAuditViewSet

router = DefaultRouter()
router.register("properties", PropertyViewSet, basename="properties")
router.register("audits", PropertyAuditViewSet, basename="audits")

urlpatterns = router.urls
