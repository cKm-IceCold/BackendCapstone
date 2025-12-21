# services.py
from .models import AuditTransaction, Property

def audit_property(auditor, property_obj, audited_price, decision, comment=""):
    audit = AuditTransaction.objects.create(
        property=property_obj,
        auditor=auditor,
        audited_price=audited_price,
        decision=decision,
        comment=comment
    )

    # Update property fields based on audit
    property_obj.price_audit_value = audited_price
    property_obj.verification_status = "verified" if decision == "approve" else "rejected"
    property_obj.save()

    return audit
