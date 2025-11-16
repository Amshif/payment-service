from abc import ABC, abstractmethod


class WebhookParserInterface(ABC):
    @abstractmethod
    def get_event_type(self, payload: dict) -> str:
        """Return normalized event type string."""
        pass

    @abstractmethod
    def get_payment_id(self, payload: dict) -> str:
        """Extract gateway-specific payment ID from webhook payload."""
        pass

    @abstractmethod
    def get_refund_id(self, payload: dict) -> str | None:
        """Extract refund ID if applicable."""
        pass
