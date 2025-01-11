from django.db import models
from django.core.validators import RegexValidator


class Customer(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(
        max_length=10,
        unique=True,
        validators=[
            RegexValidator(
                r"^[A-Z0-9]*$", "Only uppercase letters and numbers are allowed."
            )
        ],
    )
    phone_number = models.CharField(max_length=15)  # For SMS notifications
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "customers"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.code} - {self.name}"
