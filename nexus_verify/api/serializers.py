from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token
from .models import User, Property, AuditTransaction

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    token = serializers.SerializerMethodField()
    
    # Explicitly added email validation to prevent the UNIQUE constraint crash 
    # that causes the HTML error page you were seeing.
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(
            queryset=User.objects.all(),
            message="A user with this email already exists."
        )]
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'password', 'token', 'date_joined']
        read_only_fields = ['id', 'date_joined', 'token']

    def get_token(self, obj):
        # We use a try/except here to ensure that if a token 
        # doesn't exist yet, it returns None instead of crashing the response.
        try:
            return obj.auth_token.key
        except AttributeError:
            return None

    def create(self, validated_data):
        # 1. Create the user using create_user (to hash the password)
        user = User.objects.create_user(**validated_data)
        
        # 2. Immediately create the token so the 'token' field in 
        # the response has a value.
        Token.objects.create(user=user)
        
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