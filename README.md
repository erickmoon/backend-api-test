# Customer Orders API

A Django REST API for managing customers and orders with SMS notifications.

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

# For Ubuntu

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

# For macOS using Homebrew

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

# Create and activate virtual environment

```bash
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
```

# Install required packages

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

## API Endpoints Documentation

### Authentication Endpoints

- `POST /api/token/` - Obtain JWT token pair
  ```bash
  curl -X POST -H "Content-Type: application/json" -d '{"username": "your_username", "password": "your_password"}' http://localhost:8000/api/token/
  ```
- `POST /api/token/refresh/` - Refresh JWT token
  ```bash
  curl -X POST -H "Content-Type: application/json" -d '{"refresh": "your_refresh_token"}' http://localhost:8000/api/token/refresh/
  ```

### Customer Endpoints

- `GET /api/customers/` - List all customers

  ```bash
  curl -H "Authorization: Bearer your_access_token" http://localhost:8000/api/customers/
  ```

- `POST /api/customers/` - Create a new customer

  ```bash
  curl -X POST \
    -H "Authorization: Bearer your_access_token" \
    -H "Content-Type: application/json" \
    -d '{
      "name": "John Doe",
      "code": "CUST001",
      "phone_number": "+254722000000"
    }' \
    http://localhost:8000/api/customers/
  ```

- `GET /api/customers/{id}/` - Retrieve a customer

  ```bash
  curl -H "Authorization: Bearer your_access_token" http://localhost:8000/api/customers/1/
  ```

- `PUT /api/customers/{id}/` - Update a customer

  ```bash
  curl -X PUT \
    -H "Authorization: Bearer your_access_token" \
    -H "Content-Type: application/json" \
    -d '{
      "name": "John Doe Updated",
      "code": "CUST001",
      "phone_number": "+254722000000"
    }' \
    http://localhost:8000/api/customers/1/
  ```

- `DELETE /api/customers/{id}/` - Delete a customer
  ```bash
  curl -X DELETE -H "Authorization: Bearer your_access_token" http://localhost:8000/api/customers/1/
  ```

### Order Endpoints

- `GET /api/orders/` - List all orders

  ```bash
  curl -H "Authorization: Bearer your_access_token" http://localhost:8000/api/orders/
  ```

- `POST /api/orders/` - Create a new order

  ```bash
  curl -X POST \
    -H "Authorization: Bearer your_access_token" \
    -H "Content-Type: application/json" \
    -d '{
      "customer_code": "CUST001",
      "item": "Product XYZ",
      "amount": "1000.00"
    }' \
    http://localhost:8000/api/orders/
  ```

- `GET /api/orders/{id}/` - Retrieve an order

  ```bash
  curl -H "Authorization: Bearer your_access_token" http://localhost:8000/api/orders/1/
  ```

- `PUT /api/orders/{id}/` - Update an order

  ```bash
  curl -X PUT \
    -H "Authorization: Bearer your_access_token" \
    -H "Content-Type: application/json" \
    -d '{
      "customer_code": "CUST001",
      "item": "Updated Product",
      "amount": "1500.00"
    }' \
    http://localhost:8000/api/orders/1/
  ```

- `GET /api/orders/search/` - Search orders

  ```bash
  curl -H "Authorization: Bearer your_access_token" \
    "http://localhost:8000/api/orders/search/?q=Product"
  ```

- `GET /api/orders/?start_date=2024-01-01&end_date=2024-01-31` - Date range filter
  ```bash
  curl -H "Authorization: Bearer your_access_token" \
    "http://localhost:8000/api/orders/?start_date=2024-01-01&end_date=2024-01-31"
  ```

### Response Examples

#### Success Response

```json
{
  "id": 1,
  "customer_code": "CUST001",
  "customer_name": "John Doe",
  "item": "Product XYZ",
  "amount": "1000.00",
  "order_time": "2024-01-11T10:00:00Z",
  "status": "PENDING"
}
```

#### Error Response

```json
{
  "error": "Invalid customer code",
  "detail": "Customer with code CUST001 not found"
}
```

### Note

- All endpoints require JWT authentication
- Dates should be in YYYY-MM-DD format
- Customer codes must be uppercase alphanumeric
- Amount should have maximum 2 decimal places

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
