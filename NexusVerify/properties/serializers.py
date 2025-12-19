from rest_framework import serializers
from .models import Property

class PropertySerializer(serializers.ModelSerializer):
    registered_by = serializers.ReadOnlyField(source="registered_by.username")

    class Meta:
        model = Property
        fields = "__all__"
        read_only_fields = [
            "property_id",
            "verification_status",
            "price_audit_value",
            "registered_by"
        ]
