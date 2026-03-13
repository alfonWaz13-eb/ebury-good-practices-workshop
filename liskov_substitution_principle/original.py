from abc import ABC, abstractmethod
from dataclasses import dataclass


class PaymentMethod(ABC):
    @abstractmethod
    def pay(self, amount: float) -> None:
        pass

    @abstractmethod
    def refund(self, amount: float) -> None:
        pass


class CreditCardPayment(PaymentMethod):
    def pay(self, amount: float) -> None:
        print(f"Processing credit card payment of ${amount}")

    def refund(self, amount: float) -> None:
        print(f"Refunding credit card payment of ${amount}")


class ApplePayPayment(PaymentMethod):
    can_refund: bool

    def pay(self, amount: float) -> None:
        print(f"Processing Apple Pay payment of ${amount}")

    def refund(self, amount: float) -> None:
        if not self.can_refund:
            raise NotImplementedError("Refunding Apple Pay payments is not supported.")
        print(f"Refunding Apple Pay payment of ${amount}")