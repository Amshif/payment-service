import uuid
from app.services.interfaces.payment_gateway import PaymentGateway


class RazorpayClient(PaymentGateway):
    """
    Fake / Mock Razorpay Client for development and testing.
    Does NOT call the real Razorpay API.
    """

    def create_order(self, amount: int, currency: str) -> dict:
        return {
            "id": f"order_{uuid.uuid4().hex[:12]}",
            "amount": amount,
            "currency": currency,
            "status": "created",
        }

    def create_refund(self, payment_gateway_id: str, amount: int, reason: str | None = None) -> dict:
        refund_id = f"rfnd_{uuid.uuid4().hex[:12]}"

        return {
            "id": refund_id,
            "payment_id": payment_gateway_id,
            "amount": amount,
            "currency": "INR",
            "status": "processed",
            "reason": reason or "Customer requested refund",
            "created_at": str(uuid.uuid1()),
        }




# TODO: Implement real Razorpay client using razorpay SDK




# import razorpay
# from fastapi import HTTPException
# from app.core.config import settings
# from app.services.interfaces.payment_gateway import PaymentGateway


# class RazorpayClient(PaymentGateway):
#     def __init__(self):
#         """Use Pydantic Settings to load Razorpay credentials."""
#         self.client = razorpay.Client(
#             auth=(settings.RAZORPAY_KEY, settings.RAZORPAY_SECRET)
#         )

#     def create_order(self, amount: int, currency: str) -> dict:
#         try:
#             payload = {
#                 "amount": amount * 100,
#                 "currency": currency,
#                 "payment_capture": 1
#             }
#             return self.client.order.create(payload)

#         except Exception as e:
#             raise HTTPException(502, f"Razorpay order creation failed: {str(e)}")

#     def create_refund(self, payment_gateway_id: str, amount: int, reason: str | None):
#         try:
#             payload = {"amount": amount * 100}
#             if reason:
#                 payload["notes"] = {"reason": reason}

#             return self.client.payment.refund(payment_gateway_id, payload)

#         except Exception as e:
#             raise HTTPException(502, f"Razorpay refund failed: {str(e)}")
