import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from orders.models import Order
from customers.models import Customer
from decimal import Decimal


@pytest.mark.django_db
class TestOrderViews:
    @pytest.fixture
    def api_client(self):
        return APIClient()

    @pytest.fixture
    def customer(self):
        return Customer.objects.create(
            name="Test Customer", code="TEST123", phone_number="+254722000000"
        )

    @pytest.fixture
    def order_data(self, customer):
        return {"customer_code": customer.code, "item": "Test Item", "amount": "100.00"}

    def test_create_order(self, api_client, order_data):
        url = reverse("order-list-create")
        response = api_client.post(url, order_data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert Order.objects.count() == 1

    def test_search_orders(self, api_client, customer):
        Order.objects.create(
            customer=customer, item="Test Item", amount=Decimal("100.00")
        )
        url = reverse("order-search")
        response = api_client.get(url, {"q": "Test"})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
