import pytest
from django.core.exceptions import ValidationError
from customers.models import Customer


@pytest.mark.django_db
class TestCustomerModel:
    def test_create_customer_success(self):
        customer = Customer.objects.create(
            name="Test Customer", code="TEST123", phone_number="+254722000000"
        )
        assert customer.name == "Test Customer"
        assert customer.code == "TEST123"

    def test_customer_str_representation(self):
        customer = Customer.objects.create(
            name="Test Customer", code="TEST123", phone_number="+254722000000"
        )
        assert str(customer) == "TEST123 - Test Customer"

    def test_invalid_code_format(self):
        with pytest.raises(ValidationError):
            customer = Customer(
                name="Test Customer",
                code="test123",  # lowercase not allowed
                phone_number="+254722000000",
            )
            customer.full_clean()
