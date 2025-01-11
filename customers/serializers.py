from rest_framework import serializers
from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["id", "name", "code", "phone_number", "created_at"]
        read_only_fields = ["created_at"]

    def validate_code(self, value):
        """
        Check that the code is unique and follows the format
        """
        if not value.isalnum() or not value.isupper():
            raise serializers.ValidationError(
                "Code must contain only uppercase letters and numbers"
            )
        return value
