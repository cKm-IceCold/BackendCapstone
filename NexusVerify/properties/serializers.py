from rest_framework import serializers
from .models import Property
from .models import AuditTransaction
from .models import PropertyDocument

 
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


class AuditTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditTransaction
        fields = ["id", "property_obj", "auditor", "audited_price", "decision", "comment", "created_at"]
        read_only_fields = ["id", "auditor", "created_at"]


class PropertyDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyDocument
        fields = ['id', 'property_obj', 'uploaded_by', 'document', 'description', 'created_at']
        read_only_fields = ['uploaded_by', 'created_at']
