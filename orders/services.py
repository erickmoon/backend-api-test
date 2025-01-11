import africastalking
from django.conf import settings
from typing import Optional


class SMSService:
    def __init__(self):
        self.username = settings.AFRICASTALKING_USERNAME
        self.api_key = settings.AFRICASTALKING_API_KEY

        # Initialize Africa's Talking
        africastalking.initialize(self.username, self.api_key)
        self.sms = africastalking.SMS

    def send_order_confirmation(
        self, phone_number: str, order_id: int, amount: float
    ) -> Optional[str]:
        """
        Send order confirmation SMS to customer
        """
        try:
            message = f"Your order #{order_id} of amount {amount} has been received and is being processed."
            response = self.sms.send(message, [phone_number])
            return response["SMSMessageData"]["Recipients"][0]["messageId"]
        except Exception as e:
            # Log the error in production
            print(f"Error sending SMS: {str(e)}")
            return None
