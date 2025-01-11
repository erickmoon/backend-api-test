from rest_framework import serializers
from .models import Order
from customers.models import Customer


class OrderSerializer(serializers.ModelSerializer):
    customer_code = serializers.CharField(write_only=True)
    customer_name = serializers.CharField(source="customer.name", read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "customer_code",
            "customer_name",
            "item",
            "amount",
            "order_time",
            "status",
        ]
        read_only_fields = ["order_time", "status"]

    def validate_customer_code(self, value):
        try:
            Customer.objects.get(code=value)
            return value
        except Customer.DoesNotExist:
            raise serializers.ValidationError("Invalid customer code")

    def create(self, validated_data):
        customer_code = validated_data.pop("customer_code")
        customer = Customer.objects.get(code=customer_code)
        order = Order.objects.create(customer=customer, **validated_data)

        # Send SMS notification
        from .services import SMSService

        sms_service = SMSService()
        sms_service.send_order_confirmation(
            customer.phone_number, order.id, order.amount
        )

        return order
