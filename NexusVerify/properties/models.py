import uuid
from django.db import models
from django.contrib.auth.models import User

class Property(models.Model):
    ZONING_CHOICES = [
        ("approved", "Approved"),
        ("pending", "Pending"),
        ("rejected", "Rejected"),
    ]

    FRAUD_RISK_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    ]

    VERIFICATION_CHOICES = [
        ("unverified", "Unverified"),
        ("verified", "Verified"),
        ("rejected", "Rejected"),
    ]

    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    property_id = models.UUIDField(default=uuid.uuid4, unique=True)
    owner_name = models.CharField(max_length=255)

    registered_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="properties"
    )

    zoning_status = models.CharField(
        max_length=20,
        choices=ZONING_CHOICES,
        default="pending"
    )

    fraud_risk_level = models.CharField(
        max_length=20,
        choices=FRAUD_RISK_CHOICES,
        default="low"
    )

    verification_status = models.CharField(
        max_length=20,
        choices=VERIFICATION_CHOICES,
        default="unverified"
    )

    price_audit_value = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
