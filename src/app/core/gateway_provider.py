from app.utils.razorpay_client import RazorpayClient

def get_payment_gateway():
    return RazorpayClient()
