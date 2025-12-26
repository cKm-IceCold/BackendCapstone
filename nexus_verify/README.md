# Nexus Verify: Secure Property Ledger & Audited Pricing

Nexus Verify is a comprehensive real estate platform built with Django and Django REST Framework. It addresses the lack of trust in property transactions by providing a secure, audited ledger for land documents and transparent pricing valuations.

## 🚀 Overview

The platform acts as a secure intermediary layer, ensuring that all property documents, pricing, and government zoning statuses are verified by professionals before a property is listed for sale. This mitigates the risk of real estate fraud and ensures buyers are not purchasing land in illegal or government-reserved zones.

## 🛠️ Key Features

### 1. Digital Document Registry
- **Hash-Based Verification**: Real estate companies submit property documents, which are assigned unique identifiers (UUIDs/Hashes) to create a traceable digital ledger.
- **Visual Evidence**: Users can now upload and view multiple pictures of the property.
- **Immutability**: Once registered, document details provide a secure record for verification.

### 2. Role-Based Access Control (RBAC)
- **Customer**: Can browse and search for verified properties.
- **Real Estate Company**: Can register properties and upload supporting documents.
- **Auditor**: Independent professionals who review submissions, verify zoning, and assign the final "Audited Price".

### 3. Audited Pricing Workflow
- Sellers do not set the final price.
- **Workflow**: Company submits listing -> Auditor reviews -> Auditor signs off on the market valuation -> Listing becomes public.

### 4. Government Zone Verification
- Every listing includes a status badge confirming the property is in a legal, allocated area, reducing the risk of future government demolitions.

### 5. Advanced Search & Filtering
- Filter properties by location, title, audited price range, and verification status.

## 🏗️ Architecture

The project is structured into two main components to ensure scalability and separation of concerns:

- **`api/` (Backend JSON API)**: Built with Django REST Framework. Handles the core business logic, data models, and provides endpoints for mobile or external integrations.
- **`frontend/` (Web Portal)**: Built with standard Django Templates and Bootstrap for a fast, server-side rendered user experience.
- **`nexus_verify/`**: Project configuration and settings.

## 🧰 Tech Stack
- **Framework**: Django 5.2.7
- **API**: Django REST Framework (DRF)
- **Database**: SQLite (Default, easily switchable to PostgreSQL)
- **Frontend**: Django Templates with Bootstrap
- **CORS**: `django-cors-headers` enabled for cross-origin frontend systems
- **Authentication**: Supports both Session and Token Authentication

## 📥 Installation & Setup

1. **Clone the repository** (if applicable) or navigate to the project directory:
   ```bash
   cd nexus_verify
   ```

2. **Install Dependencies**:
   ```bash
   pip install django djangorestframework django-cors-headers
   ```

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

### Browser Access (Frontend Portal)
- **Registration**: Visit `/register/` to create an account. Choose your role carefully.
- **Login/Logout**: Accessible via navigation or `/login/`.
- **Properties**: Visit the root `/` to view all properties.
- **Management**: Registered users with the correct role can add, edit, or delete properties from the portal.

### API Access (Mobile/External Integration)
- **Root Endpoint**: `/api/`
- **Auth Token**: `POST /api/token/` with username and password to receive an auth token.
- **My Profile**: `/api/users/me/` - Returns the authenticated user's details and role.
- **Properties**: `/api/properties/`
- **Verification**: `/api/properties/{id}/verify/` (Auditors only)

## 🔐 Security & Configuration
- **CORS**: Configured to allow cross-origin requests (`CORS_ALLOW_ALL_ORIGINS = True` in development).
- **Permissions**: Every endpoint is protected by DRF permissions (`IsAuthenticated`, `IsAuditor`, etc.).
- **Media**: Property documents are stored in the `/media/` directory.
