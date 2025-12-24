from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import User, Property, AuditTransaction
from .serializers import UserSerializer, PropertySerializer, AuditTransactionSerializer

class IsAuditor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'AUDITOR'

class IsRealEstateCompany(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'REAL_ESTATE_COMPANY'

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = Property.objects.all()
        # Filtering
        location = self.request.query_params.get('location')
        verification_status = self.request.query_params.get('verification_status')
        fraud_risk = self.request.query_params.get('fraud_risk_level')
        zoning = self.request.query_params.get('zoning_status')
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')

        if location:
            queryset = queryset.filter(location__icontains=location)
        if verification_status:
            queryset = queryset.filter(verification_status=verification_status)
        if fraud_risk:
            queryset = queryset.filter(fraud_risk_level=fraud_risk)
        if zoning:
            queryset = queryset.filter(zoning_status=zoning)
        if min_price:
            queryset = queryset.filter(price_audit_value__gte=min_price)
        if max_price:
            queryset = queryset.filter(price_audit_value__lte=max_price)
            
        return queryset

    def perform_create(self, serializer):
        # Only Real Estate Companies can register properties? 
        # Requirement says "Real Estate Companies submit documents".
        # We'll assume anyone can for now unless strictly restricted, but let's auto-assign registered_by
        serializer.save(registered_by=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuditor])
    def verify(self, request, pk=None):
        property_obj = self.get_object()
        status_val = request.data.get('status')
        price_val = request.data.get('price_audit_value')
        notes = request.data.get('notes', '')

        if status_val not in ['VERIFIED', 'REJECTED']:
             return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

        property_obj.verification_status = status_val
        if price_val:
            property_obj.price_audit_value = price_val
        property_obj.save()

        # Create audit transaction
        AuditTransaction.objects.create(
            property=property_obj,
            auditor=request.user,
            status='APPROVED' if status_val == 'VERIFIED' else 'FLAGGED',
            notes=notes
        )

        return Response(PropertySerializer(property_obj).data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuditor])
    def reset_verification(self, request, pk=None):
        property_obj = self.get_object()
        property_obj.verification_status = 'PENDING'
        property_obj.price_audit_value = None
        property_obj.save()
        
        return Response({'status': 'Verification reset'}, status=status.HTTP_200_OK)
