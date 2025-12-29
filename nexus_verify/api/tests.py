from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User, Property
from rest_framework.authtoken.models import Token

class AuthenticationTests(APITestCase):
    def setUp(self):
        # Use a unique email for the setup user
        self.user = User.objects.create_user(
            username="setup_user",
            email="setup@example.com",
            password="password123"
        )
        self.login_url = reverse('user-login')

    def test_registration(self):
        url = reverse('user-list')
        data = {
            "email": "unique_register@example.com", # Use a unique email here
            "username": "unique_register",         # Always provide a username
            "password": "newpassword123",
            "role": "CUSTOMER"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login(self):
        """Test that a user can log in with valid credentials."""
        data = {
            "email": "setup@example.com",
            "password": "password123"
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

class PropertyTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="property_owner", 
            email="owner@example.com", 
            password="pass", 
            role="REAL_ESTATE_COMPANY"
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.url = reverse('property-list')

    def test_create_property(self):
        """Test that an authenticated user can create a property."""
        data = {
            "title": "Luxury Apartment",
            "location": "Lagos",
            "property_id": "LAG-001",
            "owner_name": "John Doe",
            "zoning_status": "Residential",
            "fraud_risk_level": "Low"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Property.objects.get(property_id="LAG-001").registered_by, self.user)