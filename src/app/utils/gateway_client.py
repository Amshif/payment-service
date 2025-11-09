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

    def create_refund(
        self, razorpay_payment_id: str, amount: int, reason: str | None = None
    ):
        """
        Simulate Razorpay refund creation.
        Returns a fake Razorpay refund object with the same structure as the real API.
        """
        # Optionally simulate random gateway errors for testing
        # Uncomment this block to test failure handling
        # if random.choice([True, False]):
        #     raise Exception("Razorpay gateway timeout")

        refund_id = f"rfnd_{uuid.uuid4().hex[:10]}"
        return {
            "id": refund_id,
            "payment_id": razorpay_payment_id,
            "amount": amount,
            "currency": "INR",
            "status": "processed",  # or 'created' depending on flow
            "reason": reason or "Customer requested refund",
            "created_at": str(uuid.uuid1()),  # placeholder timestamp
        }













# import razorpay
# from fastapi import HTTPException
# from app.core.config import settings


# class RazorpayClient:
#     """
#     Wrapper around the official Razorpay SDK for creating orders and refunds.
#     """

#     def __init__(self):
#         try:
#             self.client = razorpay.Client(auth=(settings.razorpay_key_id, settings.razorpay_key_secret))
#         except Exception as e:
#             raise HTTPException(status_code=500, detail=f"Razorpay client initialization failed: {str(e)}")

#     # ===============================
#     # Create Razorpay Order
#     # ===============================
#     def create_order(self, amount: int, currency: str = "INR", receipt: str | None = None):
#         """
#         Creates a Razorpay order.
#         Amount should be in the smallest currency unit (e.g. paise for INR).
#         """
#         try:
#             data = {
#                 "amount": amount,
#                 "currency": currency,
#                 "receipt": receipt or "txn_receipt",
#                 "payment_capture": 1,
#             }
#             order = self.client.order.create(data=data)
#             return order
#         except razorpay.errors.BadRequestError as e:
#             raise HTTPException(status_code=400, detail=f"Razorpay order creation failed: {str(e)}")
#         except Exception as e:
#             raise HTTPException(status_code=502, detail=f"Razorpay API error: {str(e)}")

#     # ===============================
#     # Create Razorpay Refund
#     # ===============================
#     def create_refund(self, razorpay_payment_id: str, amount: int, reason: str | None = None):
#         """
#         Initiates a refund on a captured Razorpay payment.
#         """
#         try:
#             data = {
#                 "amount": amount,
#                 "speed": "normal",  # can also be 'optimum' or 'instant'
#             }
#             if reason:
#                 data["notes"] = {"reason": reason}

#             refund = self.client.payment.refund(razorpay_payment_id, data)
#             return refund
#         except razorpay.errors.BadRequestError as e:
#             raise HTTPException(status_code=400, detail=f"Razorpay refund failed: {str(e)}")
#         except Exception as e:
#             raise HTTPException(status_code=502, detail=f"Razorpay refund API error: {str(e)}")
