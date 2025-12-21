from rest_framework import viewsets, permissions, filters, status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Property, AuditTransaction
from .serializers import PropertySerializer, AuditTransactionSerializer
from .permissions import IsCompanyOwner, IsAuditor
from .services import audit_property  # Function to handle audit logic


class PropertyViewSet(ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["location", "title"]
    ordering_fields = ["price_audit_value"]

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsCompanyOwner()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(registered_by=self.request.user)


class PropertyAuditViewSet(ModelViewSet):
    queryset = Property.objects.all()
    permission_classes = [IsAuthenticated, IsAuditor]

    @action(detail=True, methods=["post"])
    def audit(self, request, pk=None):
        property_obj = self.get_object()

        serializer = AuditTransactionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Service function handles audit creation and property updates
        audit = audit_property(
            auditor=request.user,
            property_obj=property_obj,
            audited_price=serializer.validated_data["audited_price"],
            decision=serializer.validated_data["decision"],
            comment=serializer.validated_data.get("comment", "")
        )

        return Response(
            AuditTransactionSerializer(audit).data,
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=["post"])
    def reset_verification(self, request, pk=None):
        property_obj = self.get_object()
        property_obj.verification_status = "unverified"
        property_obj.price_audit_value = None
        property_obj.save()
        return Response(
            {"message": "Property verification reset successfully."},
            status=status.HTTP_200_OK
        )
