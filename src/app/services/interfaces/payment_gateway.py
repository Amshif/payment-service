from abc import ABC, abstractmethod


class PaymentGateway(ABC):
    """
    Gateway contract for all payment providers (Razorpay, Stripe, PayPal)
    """

    @abstractmethod
    def create_order(self, amount: int, currency: str) -> dict:
        pass

    @abstractmethod
    def create_refund(self, payment_gateway_id: str, amount: int, reason: str | None) -> dict:
        pass
