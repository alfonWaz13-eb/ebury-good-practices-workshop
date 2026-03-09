from abc import ABC, abstractmethod
from typing import Optional


class PaymentMethod(ABC):
    @abstractmethod
    def process_payment(self, amount: float) -> bool:
        pass

    @abstractmethod
    def process_refund(self, amount: float) -> bool:
        pass

    @abstractmethod
    def get_transaction_id(self) -> str:
        pass


class CardVerifiable(ABC):
    @abstractmethod
    def verify_card(self, card_number: str) -> bool:
        pass

    @abstractmethod
    def get_card_type(self) -> str:
        pass


class OnlineMethod(ABC):
    @abstractmethod
    def send_payment_link(self, email: str) -> bool:
        pass


class CreditCardPayment(PaymentMethod, CardVerifiable, OnlineMethod):

    def process_payment(self, amount: float) -> bool:
        print(f"Processing credit card payment of ${amount}")
        return True

    def process_refund(self, amount: float) -> bool:
        print(f"Processing refund of ${amount} for transaction")
        return True

    def verify_card(self, card_number: str) -> bool:
        print(f"Verifying card number: {card_number}")
        return True

    def get_card_type(self) -> str:
        return "Visa"

    def get_transaction_id(self) -> str:
        return "txn_123456"

    def send_payment_link(self, email: str) -> bool:
        print(f"Sending payment link to {email}")
        return True


class BankTransferPayment(PaymentMethod, OnlineMethod):

    def process_payment(self, amount: float) -> bool:
        print(f"Processing bank transfer payment of ${amount}")
        return True

    def process_refund(self, amount: float) -> bool:
        print(f"Processing refund of ${amount} for account")
        return True

    def get_transaction_id(self) -> str:
        return f"BT-123456"

    def send_payment_link(self, email: str) -> bool:
        print(f"Sending bank transfer instructions to {email}")
        return True


class CashPayment(PaymentMethod):

    def process_payment(self, amount: float) -> bool:
        print(f"Processing cash payment of ${amount}")
        return True

    def process_refund(self, amount: float) -> bool:
        print(f"Processing cash refund of ${amount}")
        return True


    def get_transaction_id(self) -> str:
        return "CASH-123456"


class ApplePayPayment(PaymentMethod, CardVerifiable, OnlineMethod):

    def process_payment(self, amount: float) -> bool:
        print(f"Processing Apple Pay payment of ${amount}")
        return True

    def process_refund(self, amount: float) -> bool:
        print(f"Processing refund of ${amount} for Apple Pay")
        return True

    def verify_card(self, card_number: str) -> bool:
        print(f"Verifying virtual card number: {card_number} for Apple Pay")
        return True

    def get_card_type(self) -> str:
        print("Virtual")
        return True

    def get_transaction_id(self) -> str:
        return f"AP-123456"

    def send_payment_link(self, email: str) -> bool:
        print(f"Sending Apple Pay payment link to {email}")
        return True

    def get_payment_link(self) -> str:
        return "https://applepay.com/pay?merchant=123"
