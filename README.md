# Customer Orders API

A Django REST API for managing customers and orders with SMS notifications.

## Table of Contents

- [Overview](#overview)
- [Project Structure](#Project-Structure)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Local Development Setup](#local-development-setup)
  - [1. PostgreSQL Setup](#1-postgresql-setup)
  - [2. Project Setup](#2-project-setup)
  - [3. Database Configuration](#3-database-configuration)
  - [4. Running the Server](#4-running-the-server)
- [Docker Deployment](#docker-deployment)
- [API Documentation](#api-documentation)
  - [Authentication Endpoints](#authentication-endpoints)
  - [Customer Endpoints](#customer-endpoints)
  - [Order Endpoints](#order-endpoints)
  - [Common Error Responses](#common-error-responses)
- [Testing](#testing)
- [Security Features](#security-features)

## Overview

The Customer Orders API is a robust, production-ready REST API built with Django and Django REST Framework that manages customer data and order processing with integrated SMS notifications. This system provides a complete solution for businesses needing to track customer information and their associated orders while automatically keeping customers informed about their order status.

### Key Capabilities

- **Customer Management**: Comprehensive CRUD operations for customer profiles with validation for unique customer codes and phone numbers
- **Order Processing**: Full order lifecycle management from creation to completion
- **Real-time Notifications**: Automated SMS notifications to customers using Africa's Talking gateway
- **Search & Filtering**: Advanced search functionality for orders with date range filtering
- **Secure Authentication**: JWT-based authentication with refresh token support
- **Data Integrity**: PostgreSQL database with proper indexing and data validation
- **Scalable Architecture**: Containerized deployment ready for scaling with Docker

### Technical Stack

- **Backend Framework**: Django 5.0.1 with Django REST Framework 3.14.0
- **Database**: PostgreSQL 13+ for robust data storage
- **Authentication**: JWT (JSON Web Tokens) with refresh token mechanism
- **SMS Gateway**: Africa's Talking API integration
- **Testing**: Comprehensive test suite using pytest with 90%+ coverage
- **Containerization**: Docker and Docker Compose for consistent deployment
- **CI/CD**: Automated testing and deployment pipeline

### Design Philosophy

The API follows these core principles:

1. **RESTful Architecture**: Clear, resource-oriented endpoints following REST best practices
2. **Security First**: Implementing industry-standard security practices and data protection
3. **Scalability**: Modular design allowing for easy scaling and feature additions
4. **Maintainability**: Clean code structure with comprehensive documentation
5. **Test Coverage**: Extensive testing at unit, integration, and system levels

## Project Structure

`django_customer_orders/` - Customer Orders Management System

```plaintext
├── core/                   # Main project configuration
│   ├── settings.py        # Project settings and configurations
│   ├── urls.py            # Main URL configuration
│   └── wsgi.py            # WSGI configuration for deployment
│
├── customers/             # Customers management app
│   ├── migrations/        # Database migrations
│   ├── tests/             # Test modules
│   │   ├── test_models.py
│   │   ├── test_views.py
│   │   └── test_serializers.py
│   ├── models.py         # Customer data models
│   ├── serializers.py    # API serializers
│   ├── services.py       # Business logic services
│   ├── urls.py           # URL routing for customers
│   └── views.py          # API views and handlers
│
├── orders/               # Orders management app
│   ├── migrations/       # Database migrations
│   ├── tests/           # Test modules
│   │   ├── test_models.py
│   │   ├── test_views.py
│   │   └── test_serializers.py
│   ├── models.py        # Order data models
│   ├── serializers.py   # API serializers
│   ├── services.py      # SMS and business services
│   ├── urls.py          # URL routing for orders
│   └── views.py         # API views and handlers
│
├── docker/              # Docker configuration files
│   └── postgres/        # PostgreSQL Docker setup
│
├── static/              # Static files (CSS, JS, Images)
├── media/              # User-uploaded media files
├── templates/          # HTML templates
│
├── Dockerfile          # Docker container configuration
├── docker-compose.yml  # Docker services configuration
├── requirements.txt    # Python dependencies
├── manage.py          # Django management script
└── README.md          # Project documentation
```

This project follows a modular structure with two main apps:

- `customers`: Handles customer data and operations
- `orders`: Manages order processing and SMS notifications

Each app follows Django's recommended structure with separate files for models, views, and tests. The project uses Docker for containerization and includes configurations for PostgreSQL database.

## Features

- Customer management (CRUD operations)
- Order management with SMS notifications via Africa's Talking
- OpenID Connect authentication
- Date range-based order search
- Containerized deployment with Docker
- Automated testing and CI/CD pipeline

## Prerequisites

- Python 3.11+
- Docker and Docker Compose
- PostgreSQL 13+
- Africa's Talking account for SMS
- Git

## Local Development Setup

### 1. PostgreSQL Setup

First, install PostgreSQL if you haven't already:

For Ubuntu

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

For macOS using Homebrew

```bash
brew install postgresql
brew services start postgresql
```

Create database and user:

```bash
# Connect to PostgreSQL
sudo -u postgres psql

# Create database
CREATE DATABASE customer_orders_db;

# Create user
CREATE USER customer_orders_user WITH PASSWORD 'your_secure_password';

# Grant privileges
GRANT ALL PRIVILEGES ON DATABASE customer_orders_db TO customer_orders_user;

# Connect to the database
\c customer_orders_db

# Grant schema privileges
GRANT ALL ON SCHEMA public TO customer_orders_user;

# Exit PostgreSQL
\q
```

### 2. Python Environment Setup

Create and activate virtual environment

```bash
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
```

Install required packages

```bash

pip install -r requirements.txt

```

### 3. Project Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/customer-orders-api.git
cd customer-orders-api

# Create environment file
cp .env.example .env
```

Edit `.env` file with your configurations:

```bash
DEBUG=True
SECRET_KEY=your-secret-key-here
DB_NAME=customer_orders_db
DB_USER=customer_orders_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1
AFRICASTALKING_USERNAME=sandbox
AFRICASTALKING_API_KEY=your-api-key
OIDC_RP_CLIENT_ID=your-client-id
OIDC_RP_CLIENT_SECRET=your-client-secret
```

### 4. Initialize Database

```bash
# Apply migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### 5. Run Development Server

```bash
python manage.py runserver
```

## Docker Deployment

### 1. Build and Run with Docker

```bash
# Build and start services
docker-compose up --build

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser
```

### 2. Stopping Services

```bash
docker-compose down
```

## API Documentation

### Base URL

```
http://localhost:8000/api
```

### Authentication Endpoints

#### Obtain JWT Token

```http
POST /token/

// Request
{
    "username": "your_username",
    "password": "your_password"
}

// Success Response
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### Refresh JWT Token

```http
POST /token/refresh/

// Request
{
    "refresh": "your_refresh_token"
}

// Success Response
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Customer Endpoints

#### List All Customers

```http
GET /customers/

// Headers
Authorization: Bearer your_access_token

// Success Response
{
    "count": 2,
    "results": [
        {
            "id": 1,
            "name": "John Doe",
            "code": "CUST001",
            "phone_number": "+254722000000",
            "created_at": "2025-01-11T10:00:00Z"
        },
        {
            "id": 2,
            "name": "Jane Smith",
            "code": "CUST002",
            "phone_number": "+254722000001",
            "created_at": "2025-01-11T11:00:00Z"
        }
    ]
}
```

#### Create Customer

```http
POST /customers/

// Headers
Authorization: Bearer your_access_token
Content-Type: application/json

// Request
{
    "name": "John Doe",
    "code": "CUST001",
    "phone_number": "+254722000000"
}

// Success Response
{
    "id": 1,
    "name": "John Doe",
    "code": "CUST001",
    "phone_number": "+254722000000",
    "created_at": "2025-01-11T10:00:00Z"
}

// Error Response
{
    "code": ["Customer with this code already exists."],
    "phone_number": ["Invalid phone number format."]
}
```

#### Retrieve Customer

```http
GET /customers/{id}/

// Headers
Authorization: Bearer your_access_token

// Success Response
{
    "id": 1,
    "name": "John Doe",
    "code": "CUST001",
    "phone_number": "+254722000000",
    "created_at": "2025-01-11T10:00:00Z"
}

// Error Response
{
    "detail": "Not found."
}
```

### Order Endpoints

#### List All Orders

```http
GET /orders/

// Headers
Authorization: Bearer your_access_token

// Success Response
{
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
        },
        {
            "id": 2,
            "customer_code": "CUST002",
            "customer_name": "Jane Smith",
            "item": "Product ABC",
            "amount": "1500.00",
            "order_time": "2025-01-11T11:00:00Z",
            "status": "COMPLETED"
        }
    ]
}
```

#### Create Order

```http
POST /orders/

// Headers
Authorization: Bearer your_access_token
Content-Type: application/json

// Request
{
    "customer_code": "CUST001",
    "item": "Product XYZ",
    "amount": "1000.00"
}

// Success Response
{
    "id": 1,
    "customer_code": "CUST001",
    "customer_name": "John Doe",
    "item": "Product XYZ",
    "amount": "1000.00",
    "order_time": "2025-01-11T10:00:00Z",
    "status": "PENDING"
}

// Error Response
{
    "customer_code": ["Invalid customer code."],
    "amount": ["Ensure that there are no more than 2 decimal places."]
}
```

#### Search Orders

```http
GET /orders/search/?q=Product

// Headers
Authorization: Bearer your_access_token

// Success Response
{
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

#### Filter Orders by Date Range

```http
GET /orders/?start_date=2025-01-01&end_date=2025-01-31

// Headers
Authorization: Bearer your_access_token

// Success Response
{
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
        },
        {
            "id": 2,
            "customer_code": "CUST002",
            "customer_name": "Jane Smith",
            "item": "Product ABC",
            "amount": "1500.00",
            "order_time": "2025-01-15T11:00:00Z",
            "status": "COMPLETED"
        }
    ]
}

// Error Response
{
    "error": "Invalid date format. Use YYYY-MM-DD"
}
```

### Common Error Responses

```http
// Authentication Error
{
    "detail": "Authentication credentials were not provided."
}

// Permission Error
{
    "detail": "You do not have permission to perform this action."
}

// Validation Error
{
    "field_name": [
        "Error message details"
    ]
}

// Not Found Error
{
    "detail": "Not found."
}
```

### Important Notes

- All endpoints require JWT authentication via Bearer token
- Dates must be in YYYY-MM-DD format
- Customer codes must be uppercase alphanumeric (e.g., CUST001)
- Amount values support up to 2 decimal places (e.g., 1000.00)
- Phone numbers must be in international format (e.g., +254722000000)
- All timestamps are returned in ISO 8601 format with UTC timezone

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
├── customers
│   └── tests
│       ├── test_models.py
│       ├── test_views.py
│       └── test_serializers.py
└── orders
    └── tests
        ├── test_models.py
        ├── test_views.py
        └── test_serializers.py
```

## Authentication

This API uses OpenID Connect for authentication. Include the Bearer token in the Authorization header:

```
Authorization: Bearer <your_token>
```

### Token Generation

1. Configure your OpenID Connect provider in settings.py
2. Obtain tokens through your provider's authentication flow
3. Use the access token in API requests

## Security Features

- SQL Injection Protection: Using Django's ORM and parameterized queries
- XSS Protection: Django's template system and DRF's serializers
- CSRF Protection: Django's CSRF middleware
- Rate Limiting: Using DRF's throttling
- Input Validation: Through serializers and model validators
- Database Connection Security: SSL/TLS enabled
- Password Hashing: Django's password hashing system
- CORS Configuration: Controlled cross-origin resource sharing
