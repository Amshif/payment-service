import uuid

class RazorpayClient:
    def create_order(self, amount: int, currency: str):
        """Simulate Razorpay order creation"""
        return {
            "id": f"order_{uuid.uuid4().hex[:10]}",
            "amount": amount,
            "currency": currency,
            "status": "created",
        }
