from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # Make email unique and required
    email = models.EmailField(unique=True) 
    
    ROLE_CHOICES = (
        ('CUSTOMER', 'Customer'),
        ('REAL_ESTATE_COMPANY', 'Real Estate Company'),
        ('AUDITOR', 'Auditor'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='CUSTOMER')
    created_at = models.DateTimeField(auto_now_add=True)

    # ADD THESE TWO LINES:
    USERNAME_FIELD = 'email'      # This makes email the unique identifier for login
    REQUIRED_FIELDS = ['username'] # username is still required for createsuperuser

 

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

class Property(models.Model):
    VERIFICATION_STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('VERIFIED', 'Verified'),
        ('REJECTED', 'Rejected'),
    )
    
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    property_id = models.CharField(max_length=50, unique=True)
    owner_name = models.CharField(max_length=255)
    registered_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='registered_properties')
    zoning_status = models.CharField(max_length=100)
    fraud_risk_level = models.CharField(max_length=50) # e.g., Low, Medium, High
    verification_status = models.CharField(max_length=20, choices=VERIFICATION_STATUS_CHOICES, default='PENDING')
    price_audit_value = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    document = models.FileField(upload_to='property_documents/', null=True, blank=True)
    image = models.ImageField(upload_to='property_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.property_id})"

class AuditTransaction(models.Model):
    AUDIT_STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('FLAGGED', 'Flagged'),
    )

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='audits')
    auditor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='audits_performed')
    status = models.CharField(max_length=20, choices=AUDIT_STATUS_CHOICES, default='PENDING')
    notes = models.TextField(blank=True)
    audit_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Audit for {self.property.property_id} by {self.auditor.username}"
