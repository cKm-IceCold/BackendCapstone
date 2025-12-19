from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Property
from .serializers import PropertySerializer
from .services import create_property, update_property
from .permissions import IsCompany, IsOwner

class PropertyViewSet(ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        elif self.action == "create":
            return [IsAuthenticated(), IsCompany()]
        elif self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsCompany(), IsOwner()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        create_property(self.request.user, serializer.validated_data)
