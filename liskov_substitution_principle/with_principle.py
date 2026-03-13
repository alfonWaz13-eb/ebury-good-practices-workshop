from abc import ABC, abstractmethod
from dataclasses import dataclass


class PaymentMethod(ABC):
    @abstractmethod
    def pay(self, amount: float) -> bool:
        pass

    @abstractmethod
    def refund(self, amount: float) -> bool:
        pass


class CreditCardPayment(PaymentMethod):
    def pay(self, amount: float) -> bool:
        print(f"Processing credit card payment of ${amount}")
        return True

    def refund(self, amount: float) -> bool:
        print(f"Refunding credit card payment of ${amount}")
        return True


class ApplePayPayment(PaymentMethod):
    can_refund: bool

    def pay(self, amount: float) -> bool:
        print(f"Processing Apple Pay payment of ${amount}")
        return True

    def refund(self, amount: float) -> bool:
        if not self.can_refund:
            return False
        print(f"Refunding Apple Pay payment of ${amount}")
        return True
