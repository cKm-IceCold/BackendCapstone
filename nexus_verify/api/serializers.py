from rest_framework import serializers
from .models import User, Property, AuditTransaction

from rest_framework.authtoken.models import Token

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'password', 'token', 'date_joined']
        read_only_fields = ['id', 'date_joined', 'token']

    def get_token(self, obj):
        token, created = Token.objects.get_or_create(user=obj)
        return token.key

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

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
