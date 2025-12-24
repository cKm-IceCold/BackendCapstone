from rest_framework import serializers
from .models import User, Property, AuditTransaction

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'date_joined']
        read_only_fields = ['id', 'date_joined']

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'
        read_only_fields = ['id', 'registered_by', 'verification_status', 'created_at']

class AuditTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditTransaction
        fields = '__all__'
        read_only_fields = ['id', 'auditor', 'audit_date']
