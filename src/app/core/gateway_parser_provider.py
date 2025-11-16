from app.services.webhooks.parsers.razorpay_parser import RazorpayWebhookParser


def get_webhook_parser():
    """
    Returns parser based on detected gateway.
    For now always Razorpay.
    Later: auto-detect from headers.
    """
    return RazorpayWebhookParser()