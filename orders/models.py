from django.db import models
from customers.models import Customer
from django.core.validators import MinValueValidator
from decimal import Decimal


class Order(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="orders"
    )
    item = models.CharField(max_length=100)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))]
    )
    order_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ("PENDING", "Pending"),
            ("COMPLETED", "Completed"),
            ("CANCELLED", "Cancelled"),
        ],
        default="PENDING",
    )

    class Meta:
        db_table = "orders"
        ordering = ["-order_time"]
        indexes = [
            models.Index(fields=["order_time"]),
            models.Index(fields=["customer"]),
        ]

    def __str__(self):
        return f"Order {self.id} - {self.customer.name} - {self.amount}"
