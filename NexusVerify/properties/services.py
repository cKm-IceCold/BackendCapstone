from .models import AuditTransaction, Property

def audit_property(auditor, property_obj, audited_price, decision, comment=""):
    # Create audit transaction
    audit = AuditTransaction.objects.create(
        auditor=auditor,
        property_obj=property_obj,
        audited_price=audited_price,
        decision=decision,
        comment=comment
    )

    # Update property based on audit
    if decision == "approved":
        property_obj.verification_status = "verified"
        property_obj.price_audit_value = audited_price
    elif decision == "rejected":
        property_obj.verification_status = "rejected"
    else:
        property_obj.verification_status = "unverified"

    property_obj.save()
    return audit
