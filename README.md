# Customer Orders API

A Django REST API for managing customers and orders with integrated SMS notifications and OpenID Connect authentication.

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Local Development Setup](#local-development-setup)
- [Docker Deployment](#docker-deployment)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Security Features](#security-features)

## Overview

The Customer Orders API is a robust, production-ready REST API built with Django and Django REST Framework that manages customer data and order processing with integrated SMS notifications. This system provides a complete solution for businesses needing to track customer information and their associated orders while automatically keeping customers informed about their order status.

### Key Capabilities

- **Customer Management**: CRUD operations for customer profiles with validation
- **Order Processing**: Full order lifecycle management from creation to completion
- **Real-time Notifications**: Automated SMS notifications via Africa's Talking gateway
- **Search & Filtering**: Advanced search functionality for orders with date range filtering
- **Secure Authentication**: OpenID Connect authentication integration
- **Data Integrity**: PostgreSQL database with proper indexing and data validation
- **Scalable Architecture**: Docker containerization for easy deployment and scaling

### Technical Stack

- **Backend Framework**: Django 5.0.1 with Django REST Framework 3.14.0
- **Database**: PostgreSQL 13+
- **Authentication**: OpenID Connect via mozilla-django-oidc
- **SMS Gateway**: Africa's Talking API
- **Testing**: pytest with coverage reporting
- **Documentation**: OpenAPI/Swagger specification
- **Containerization**: Docker and Docker Compose
- **CI/CD**: Automated testing and deployment pipeline

## Project Structure

```plaintext
django_customer_orders/
├── core/                   # Main project configuration
│   ├── authentication/     # Authentication configuration
│   │   ├── backend.py     # Custom OIDC authentication backend
│   │   └── middleware.py  # Authentication middleware
│   ├── settings.py        # Project settings
│   ├── urls.py            # Main URL routing
│   └── wsgi.py            # WSGI configuration
│
├── customers/             # Customers management app
│   ├── migrations/        # Database migrations
│   ├── tests/            # Test modules
│   │   ├── test_models.py
│   │   ├── test_views.py
│   │   └── test_serializers.py
│   ├── admin.py          # Admin interface configuration
│   ├── models.py         # Customer data models
│   ├── serializers.py    # API serializers
│   ├── services.py       # Business logic
│   ├── urls.py           # URL routing
│   └── views.py          # API views
│
├── orders/               # Orders management app
│   ├── migrations/       # Database migrations
│   ├── tests/           # Test modules
│   │   ├── test_models.py
│   │   ├── test_views.py
│   │   └── test_serializers.py
│   ├── admin.py         # Admin interface configuration
│   ├── models.py        # Order data models
│   ├── serializers.py   # API serializers
│   ├── services.py      # SMS and business services
│   ├── urls.py          # URL routing
│   └── views.py         # API views
│
├── docker/              # Docker configuration files
│   └── postgres/        # PostgreSQL Docker config
├── media/              # Media files storage
├── static/             # Static files
├── templates/          # HTML templates
├── Dockerfile         # Docker container configuration
├── docker-compose.yml # Docker services configuration
├── manage.py          # Django management script
└── requirements.txt   # Python dependencies
```

## Features

- Customer management (CRUD operations)
- Order management with SMS notifications
- OpenID Connect authentication
- Date range-based order search
- Containerized deployment
- Automated testing and CI/CD pipeline

## Prerequisites

- Python 3.11+
- PostgreSQL 13+
- Docker and Docker Compose
- Africa's Talking account
- OpenID Connect Provider (e.g., Auth0, Okta)
- Git

## Local Development Setup

### PostgreSQL Setup

```bash
# Install PostgreSQL
brew install postgresql  # macOS
brew services start postgresql

# Create Database and User
psql postgres
CREATE DATABASE customer_orders_db;
CREATE USER customer_orders_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE customer_orders_db TO customer_orders_user;
\c customer_orders_db
GRANT ALL ON SCHEMA public TO customer_orders_user;
\q
```

### Project Setup

```bash
# Clone repository
git clone https://github.com/yourusername/django_customer_orders.git
cd django_customer_orders

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Environment Configuration

Create `.env` file:

```bash
DEBUG=True
SECRET_KEY=<your-generated-django-secret-key>

# Database
DB_NAME=customer_orders_db
DB_USER=customer_orders_user
DB_PASSWORD=<your-database-password>
DB_HOST=localhost
DB_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1

# Africas Talking
AFRICASTALKING_USERNAME=sandbox
AFRICASTALKING_API_KEY=<your-africas-talking-api-key>

# Auth0 OIDC Settings
OIDC_RP_CLIENT_ID=<your-auth0-client-id>
OIDC_RP_CLIENT_SECRET=<your-auth0-client-secret>
OIDC_OP_AUTHORIZATION_ENDPOINT=https://<your-auth0-domain>/authorize
OIDC_OP_TOKEN_ENDPOINT=https://<your-auth0-domain>/oauth/token
OIDC_OP_USER_ENDPOINT=https://<your-auth0-domain>/userinfo
OIDC_OP_JWKS_ENDPOINT=https://<your-auth0-domain>/.well-known/jwks.json
```

### Database Initialization

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### Run Development Server

```bash
python manage.py runserver
```

## Docker Deployment

### Build and Run Services

```bash
# Build and start services
docker-compose up --build

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser
```

### Stop Services

```bash
docker-compose down
```

## API Documentation

### Authentication

The API uses OpenID Connect (OIDC) for authentication via Auth0. You'll need to:

1. **Get Auth0 Credentials**:

   - Create an Auth0 account
   - Create a new application
   - Get your Client ID and Client Secret
   - Configure allowed callback URLs

2. **Authentication Flow**:

```bash
# 1. Redirect user to Auth0 login
GET https://<your-auth0-domain>/authorize
?response_type=code
&client_id=<your-client-id>
&redirect_uri=<your-callback-url>
&scope=openid profile email

# 2. Exchange code for tokens
POST https://<your-auth0-domain>/oauth/token
{
    "grant_type": "authorization_code",
    "client_id": "<your-client-id>",
    "client_secret": "<your-client-secret>",
    "code": "<code-from-callback>",
    "redirect_uri": "<your-callback-url>"
}

# 3. Response with tokens
{
    "access_token": "<your-access-token>",
    "id_token": "<your-id-token>",
    "token_type": "Bearer",
    "expires_in": 86400
}
```

3. **Using the Token**:

```bash
GET /api/customers/
Authorization: Bearer <your-access-token>
```

4. **Error Responses**:

```bash
# Invalid or expired token
{
    "status": "error",
    "message": "Token is invalid or has expired",
    "code": "invalid_token"
}

# Missing token
{
    "status": "error",
    "message": "Authorization header is missing",
    "code": "no_token"
}

# Invalid authorization header format
{
    "status": "error",
    "message": "Invalid authorization header format",
    "code": "invalid_header"
}
```

### Customer Endpoints

#### List Customers

```http
GET /api/customers/

// Success Response
{
    "status": "success",
    "count": 2,
    "results": [
        {
            "id": 1,
            "name": "John Doe",
            "code": "CUST001",
            "phone_number": "+254722000000",
            "created_at": "2025-01-11T10:00:00Z"
        }
    ]
}
```

#### Create Customer

```http
POST /api/customers/

// Request
{
    "name": "John Doe",
    "code": "CUST001",
    "phone_number": "+254722000000"
}

// Success Response
{
    "status": "success",
    "message": "Customer created successfully",
    "data": {
        "id": 1,
        "name": "John Doe",
        "code": "CUST001",
        "phone_number": "+254722000000",
        "created_at": "2025-01-11T10:00:00Z"
    }
}
```

#### Retrieve Customer

```http
GET /api/customers/{id}/

// Success Response
{
    "status": "success",
    "data": {
        "id": 1,
        "name": "John Doe",
        "code": "CUST001",
        "phone_number": "+254722000000",
        "created_at": "2025-01-11T10:00:00Z"
    }
}
```

### Order Endpoints

#### List Orders

```http
GET /api/orders/

// Success Response
{
    "status": "success",
    "count": 2,
    "results": [
        {
            "id": 1,
            "customer_code": "CUST001",
            "customer_name": "John Doe",
            "item": "Product XYZ",
            "amount": "1000.00",
            "order_time": "2025-01-11T10:00:00Z",
            "status": "PENDING"
        }
    ]
}
```

#### Create Order

```http
POST /api/orders/

// Request
{
    "customer_code": "CUST001",
    "item": "Product XYZ",
    "amount": "1000.00"
}

// Success Response
{
    "status": "success",
    "message": "Order created successfully",
    "data": {
        "id": 1,
        "customer_code": "CUST001",
        "customer_name": "John Doe",
        "item": "Product XYZ",
        "amount": "1000.00",
        "order_time": "2025-01-11T10:00:00Z",
        "status": "PENDING"
    }
}
```

#### Search Orders

```http
GET /api/orders/search/?q=Product

// Success Response
{
    "status": "success",
    "count": 1,
    "results": [
        {
            "id": 1,
            "customer_code": "CUST001",
            "customer_name": "John Doe",
            "item": "Product XYZ",
            "amount": "1000.00",
            "order_time": "2025-01-11T10:00:00Z",
            "status": "PENDING"
        }
    ]
}
```

#### Filter Orders by Date

```http
GET /api/orders/?start_date=2025-01-01&end_date=2025-01-31

// Success Response
{
    "status": "success",
    "count": 2,
    "results": [...]
}
```

### Common Error Responses

```http
// Authentication Error
{
    "status": "error",
    "message": "Authentication credentials were not provided."
}

// Permission Error
{
    "status": "error",
    "message": "You do not have permission to perform this action."
}

// Validation Error
{
    "status": "error",
    "errors": {
        "field_name": ["Error message details"]
    }
}

// Not Found Error
{
    "status": "error",
    "message": "Resource not found"
}
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=.

# Generate coverage report
pytest --cov=. --cov-report=html
```

### Test Structure

```
├── customers/tests/
│   ├── test_models.py
│   ├── test_views.py
│   └── test_serializers.py
└── orders/tests/
    ├── test_models.py
    ├── test_views.py
    └── test_serializers.py
```

## Security Features

- OpenID Connect Authentication
- SQL Injection Protection (Django ORM)
- XSS Protection (DRF Serializers)
- CSRF Protection (Django Middleware)
- Rate Limiting (DRF Throttling)
- Input Validation (Serializers)
- Secure Database Connection (SSL/TLS)
- Password Hashing (Django Auth)
- CORS Configuration
- Logging and Monitoring
- Request/Response Validation
- Error Handling

### Security Best Practices

1. All endpoints require authentication
2. Validation on all input data
3. Proper error handling and logging
4. Secure configuration settings
5. Regular security updates
6. Database connection encryption
7. API rate limiting
8. Input sanitization
9. Secure password storage
10. CORS policy enforcement
