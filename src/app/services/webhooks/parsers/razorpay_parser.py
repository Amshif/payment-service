from .base import WebhookParserInterface


class RazorpayWebhookParser(WebhookParserInterface):
    def get_event_type(self, payload: dict) -> str:
        return payload.get("event")

    def get_payment_id(self, payload: dict) -> str:
        try:
            return payload["payload"]["payment"]["entity"]["id"]
        except Exception:
            return None

    def get_refund_id(self, payload: dict) -> str | None:
        try:
            return payload["payload"]["refund"]["entity"]["id"]
        except Exception:
            return None
