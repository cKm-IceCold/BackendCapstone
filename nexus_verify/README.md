# Nexus Verify: Secure Property Ledger & Audited Pricing

Nexus Verify is a comprehensive real estate platform built with Django and Django REST Framework. It addresses the lack of trust in property transactions by providing a secure, audited ledger for land documents and transparent pricing valuations.

## 🚀 Overview

The platform acts as a secure intermediary layer, ensuring that all property documents, pricing, and government zoning statuses are verified by professionals before a property is listed for sale. This mitigates the risk of real estate fraud and ensures buyers are not purchasing land in illegal or government-reserved zones.

## 🛠️ Key Features

### 1. Digital Document Registry
- **Property Registration**: Real Estate Companies and registered users can submit property details including title, location, and owner name.
- **Document & Image Upload**: Supports uploading a property document (file) and a property image to provide visual evidence.
- **Tracking**: Each property is assigned a unique `property_id` for easy tracking.

### 2. Role-Based Access Control (RBAC)
The system employs a custom User model with specific roles:
- **Customer**: Can browse and search for verified properties.
- **Real Estate Company**: Can register properties and upload supporting documents.
- **Auditor**: Independent professionals who review submissions, verify zoning, and assign the final "Audited Price".

### 3. Audited Pricing Workflow
- Sellers do not set the final displayed price.
- **Workflow**: 
  1. Property is registered (Default status: `PENDING`).
  2. Auditor reviews the submission via the API.
  3. Auditor verifies the property, sets the `price_audit_value`, and updates status to `VERIFIED` (or `REJECTED`).
  4. An `AuditTransaction` record is created to log the auditor's action.

### 4. Government Zone Verification
- Properties include a `zoning_status` and `fraud_risk_level` (e.g., Low, Medium, High).
- These details are input during registration and verified by Auditors to ensure compliance with government regulations.

### 5. Advanced Search & Filtering
- **Frontend**: Search properties by location or title.
- **API**: Advanced filtering by:
    - Location
    - Verification Status (`PENDING`, `VERIFIED`, `REJECTED`)
    - Fraud Risk Level
    - Zoning Status
    - Price Range (`min_price`, `max_price`)

## 🏗️ Architecture

The project is structured into two main components:

- **`api/` (Backend JSON API)**: 
    - Built with Django REST Framework.
    - Handles core business logic, data models (`User`, `Property`, `AuditTransaction`), and permissions.
    - Exposes endpoints for identifying users, managing properties, and performing audits.
- **`frontend/` (Web Portal)**: 
    - Built with standard Django Templates and Bootstrap.
    - Provides a server-side rendered interface for User Registration, Login, and Property CRUD operations.
- **`nexus_verify/`**: 
    - Project configuration, settings, and URL routing.

## 🧰 Tech Stack
- **Framework**: Django 5.x
- **API**: Django REST Framework (DRF)
- **Database**: SQLite (Default)
- **Frontend**: Django Templates, Bootstrap
- **Authentication**: Session Auth (Frontend) & Token Auth (API)

## 📥 Installation & Setup

1. **Navigate to the project directory**:
   ```bash
   cd nexus_verify
   ```

2. **Install Dependencies**:
   ```bash
   pip install django djangorestframework django-cors-headers pillow
   ```
   *(Note: `pillow` is required for ImageField)*

3. **Apply Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create a Superuser** (for Admin access):
   ```bash
   python manage.py createsuperuser
   ```

5. **Start the Development Server**:
   ```bash
   python manage.py runserver
   ```

## 📖 Usage Guide

### Frontend Portal
- **Register**: `/register/` - Create an account as Customer, Real Estate Company, or Auditor.
- **Login**: `/login/`
- **Properties**: `/` - View all properties. Authenticated users can create new listings.
- **Management**: Edit or delete properties you created.

### API Access
- **Base URL**: `/api/`
- **Authentication**: `POST /api/token/` (if configured) or Session Auth.
- **Current User**: `GET /api/users/me/`
- **Properties**: 
    - `GET /api/properties/` - List all properties (supports query params for filtering).
    - `POST /api/properties/` - Create a new property.
- **Auditing (Auditors Only)**:
    - `POST /api/properties/{id}/verify/`
      - Body: `{"status": "VERIFIED", "price_audit_value": 500000, "notes": "All documents valid."}`
    - `POST /api/properties/{id}/reset_verification/`

## 🔐 Security & Permissions
- **IsAuthenticated**: Required for most write operations.
- **IsAuditor**: Custom permission required for verifying properties.
- **IsRealEstateCompany**: Permission class available for future restrictions.
- **Object Permissions**: Users can only edit/delete properties they registered (unless they are superusers/auditors depending on specific view logic).
