from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from mozilla_django_oidc.contrib.drf import OIDCAuthentication
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from .models import Order
from .serializers import OrderSerializer
from datetime import datetime
from django.db.models import Q
import logging

logger = logging.getLogger(__name__)


class OrderListCreateView(APIView):
    authentication_classes = [OIDCAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        List all orders with optional date range filtering.

        Query Parameters:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)

        Returns:
            Response: List of filtered orders
        """
        try:
            start_date = request.query_params.get("start_date")
            end_date = request.query_params.get("end_date")

            orders = Order.objects.all()

            if start_date and end_date:
                try:
                    start_date = datetime.strptime(start_date, "%Y-%m-%d")
                    end_date = datetime.strptime(end_date, "%Y-%m-%d")
                    orders = orders.filter(
                        order_time__date__range=[start_date, end_date]
                    )
                except ValueError:
                    return Response(
                        {
                            "status": "error",
                            "message": "Invalid date format. Use YYYY-MM-DD",
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            serializer = OrderSerializer(orders, many=True)
            return Response(
                {
                    "status": "success",
                    "count": len(serializer.data),
                    "results": serializer.data,
                }
            )
        except Exception as e:
            logger.error(f"Error fetching orders: {str(e)}")
            return Response(
                {"status": "error", "message": "Failed to fetch orders"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def post(self, request):
        """
        Create a new order.

        Returns:
            Response: Created order data or error message
        """
        try:
            serializer = OrderSerializer(data=request.data)
            if serializer.is_valid():
                order = serializer.save()
                logger.info(f"Created new order for customer: {order.customer.code}")
                return Response(
                    {
                        "status": "success",
                        "message": "Order created successfully",
                        "data": serializer.data,
                    },
                    status=status.HTTP_201_CREATED,
                )
            return Response(
                {"status": "error", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            logger.error(f"Error creating order: {str(e)}")
            return Response(
                {"status": "error", "message": "Failed to create order"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class OrderDetailView(APIView):
    authentication_classes = [OIDCAuthentication]
    permission_classes = [IsAuthenticated]

    def get_order(self, pk):
        """Helper method to get order or raise 404"""
        return get_object_or_404(Order, pk=pk)

    def get(self, request, pk):
        """
        Retrieve an order by ID.

        Args:
            pk: Order ID

        Returns:
            Response: Order details or error message
        """
        try:
            order = self.get_order(pk)
            serializer = OrderSerializer(order)
            return Response({"status": "success", "data": serializer.data})
        except Order.DoesNotExist:
            return Response(
                {"status": "error", "message": "Order not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            logger.error(f"Error retrieving order {pk}: {str(e)}")
            return Response(
                {"status": "error", "message": "Failed to retrieve order"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class OrderSearchView(APIView):
    authentication_classes = [OIDCAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Search orders by query string.

        Query Parameters:
            q: Search query string

        Returns:
            Response: List of matching orders
        """
        try:
            query = request.query_params.get("q", "")
            orders = Order.objects.filter(
                Q(customer__name__icontains=query)
                | Q(customer__code__icontains=query)
                | Q(item__icontains=query)
            )
            serializer = OrderSerializer(orders, many=True)
            return Response(
                {
                    "status": "success",
                    "count": len(serializer.data),
                    "results": serializer.data,
                }
            )
        except Exception as e:
            logger.error(f"Error searching orders: {str(e)}")
            return Response(
                {"status": "error", "message": "Failed to search orders"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
