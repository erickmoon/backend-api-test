import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from customers.models import Customer


@pytest.mark.django_db
class TestCustomerViews:
    @pytest.fixture
    def api_client(self):
        return APIClient()

    @pytest.fixture
    def customer_data(self):
        return {
            "name": "Test Customer",
            "code": "TEST123",
            "phone_number": "+254722000000",
        }

    def test_create_customer(self, api_client, customer_data):
        url = reverse("customer-list-create")
        response = api_client.post(url, customer_data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert Customer.objects.count() == 1
        assert Customer.objects.get().name == "Test Customer"

    def test_get_customer_list(self, api_client, customer_data):
        Customer.objects.create(**customer_data)
        url = reverse("customer-list-create")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
