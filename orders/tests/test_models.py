import pytest
from decimal import Decimal
from orders.models import Order
from customers.models import Customer


@pytest.mark.django_db
class TestOrderModel:
    @pytest.fixture
    def customer(self):
        return Customer.objects.create(
            name="Test Customer", code="TEST123", phone_number="+254722000000"
        )

    def test_create_order_success(self, customer):
        order = Order.objects.create(
            customer=customer, item="Test Item", amount=Decimal("100.00")
        )
        assert order.item == "Test Item"
        assert order.amount == Decimal("100.00")
        assert order.status == "PENDING"

    def test_order_str_representation(self, customer):
        order = Order.objects.create(
            customer=customer, item="Test Item", amount=Decimal("100.00")
        )
        assert str(order) == f"Order {order.id} - Test Customer - 100.00"
