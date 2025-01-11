from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from mozilla_django_oidc.contrib.drf import OIDCAuthentication
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from .models import Customer
from .serializers import CustomerSerializer
from django.db import IntegrityError
import logging

logger = logging.getLogger(__name__)


class CustomerListCreateView(APIView):
    authentication_classes = [OIDCAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        List all customers.

        Returns:
            Response: List of all customers with their details
        """
        try:
            customers = Customer.objects.all()
            serializer = CustomerSerializer(customers, many=True)
            return Response(
                {
                    "status": "success",
                    "count": len(serializer.data),
                    "results": serializer.data,
                }
            )
        except Exception as e:
            logger.error(f"Error fetching customers: {str(e)}")
            return Response(
                {"status": "error", "message": "Failed to fetch customers"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def post(self, request):
        """
        Create a new customer.

        Args:
            request: HTTP request containing customer data

        Returns:
            Response: Created customer data or error messages
        """
        try:
            serializer = CustomerSerializer(data=request.data)
            if serializer.is_valid():
                customer = serializer.save()
                logger.info(f"Created new customer: {customer.code}")
                return Response(
                    {
                        "status": "success",
                        "message": "Customer created successfully",
                        "data": serializer.data,
                    },
                    status=status.HTTP_201_CREATED,
                )

            return Response(
                {"status": "error", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except IntegrityError as e:
            logger.error(f"Database integrity error: {str(e)}")
            return Response(
                {
                    "status": "error",
                    "message": "Customer with this code already exists",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            logger.error(f"Error creating customer: {str(e)}")
            return Response(
                {"status": "error", "message": "Failed to create customer"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class CustomerDetailView(APIView):
    authentication_classes = [OIDCAuthentication]
    permission_classes = [IsAuthenticated]

    def get_customer(self, pk):
        """Helper method to get customer or raise 404"""
        return get_object_or_404(Customer, pk=pk)

    def get(self, request, pk):
        """
        Retrieve a customer by ID.

        Args:
            pk: Customer ID

        Returns:
            Response: Customer details or error message
        """
        try:
            customer = self.get_customer(pk)
            serializer = CustomerSerializer(customer)
            return Response({"status": "success", "data": serializer.data})
        except Customer.DoesNotExist:
            return Response(
                {"status": "error", "message": "Customer not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            logger.error(f"Error retrieving customer {pk}: {str(e)}")
            return Response(
                {"status": "error", "message": "Failed to retrieve customer"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def put(self, request, pk):
        """
        Update a customer by ID.

        Args:
            pk: Customer ID
            request: HTTP request containing updated data

        Returns:
            Response: Updated customer data or error message
        """
        try:
            customer = self.get_customer(pk)
            serializer = CustomerSerializer(customer, data=request.data)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"Updated customer: {customer.code}")
                return Response(
                    {
                        "status": "success",
                        "message": "Customer updated successfully",
                        "data": serializer.data,
                    }
                )
            return Response(
                {"status": "error", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Customer.DoesNotExist:
            return Response(
                {"status": "error", "message": "Customer not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            logger.error(f"Error updating customer {pk}: {str(e)}")
            return Response(
                {"status": "error", "message": "Failed to update customer"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def delete(self, request, pk):
        """
        Delete a customer by ID.

        Args:
            pk: Customer ID

        Returns:
            Response: Success message or error message
        """
        try:
            customer = self.get_customer(pk)
            customer_code = customer.code
            customer.delete()
            logger.info(f"Deleted customer: {customer_code}")
            return Response(
                {"status": "success", "message": "Customer deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Customer.DoesNotExist:
            return Response(
                {"status": "error", "message": "Customer not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            logger.error(f"Error deleting customer {pk}: {str(e)}")
            return Response(
                {"status": "error", "message": "Failed to delete customer"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
