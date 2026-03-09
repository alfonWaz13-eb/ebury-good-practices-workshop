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
    def verify_card(self, card_number: str) -> bool:
        pass

    @abstractmethod
    def get_card_type(self) -> str:
        pass

    @abstractmethod
    def get_transaction_id(self) -> str:
        pass

    @abstractmethod
    def send_payment_link(self, email: str) -> bool:
        pass


class CreditCardPayment(PaymentMethod):
    def __init__(self, card_number: str, cvv: str):
        self.card_number = card_number
        self.cvv = cvv
        self.last_transaction_id: Optional[str] = None

    def process_payment(self, amount: float) -> bool:
        print(f"Processing credit card payment of ${amount}")
        self.last_transaction_id = "txn_123456"
        return True

    def process_refund(self, amount: float) -> bool:
        print(f"Processing refund of ${amount} for transaction {self.last_transaction_id}")
        return True

    def verify_card(self, card_number: str) -> bool:
        print(f"Verifying card number: {card_number}")
        return True

    def get_card_type(self) -> str:
        return "Visa"

    def get_transaction_id(self) -> str:
        return self.last_transaction_id or "No transaction"

    def send_payment_link(self, email: str) -> bool:
        print(f"Sending payment link to {email}")
        return True


class BankTransferPayment(PaymentMethod):
    def __init__(self, account_number: str, bank_code: str):
        self.account_number = account_number
        self.bank_code = bank_code

    def process_payment(self, amount: float) -> bool:
        print(f"Processing bank transfer payment of ${amount}")
        return True

    def process_refund(self, amount: float) -> bool:
        print(f"Processing refund of ${amount} for account {self.account_number}")
        return True

    def verify_card(self, card_number: str) -> bool:
        raise NotImplementedError("BankTransferPayment does not support card verification")

    def get_card_type(self) -> str:
        raise NotImplementedError("BankTransferPayment does not have a card type")

    def get_transaction_id(self) -> str:
        return f"BT-{self.account_number}-123456"

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

    def verify_card(self, card_number: str) -> bool:
        raise NotImplementedError("CashPayment does not support card verification")

    def get_card_type(self) -> str:
        raise NotImplementedError("CashPayment does not have a card type")

    def get_transaction_id(self) -> str:
        return "CASH-123456"

    def send_payment_link(self, email: str) -> bool:
        raise NotImplementedError("CashPayment does not support sending payment links")


class ApplePayPayment(PaymentMethod):
    def __init__(self, merchant_id: str):
        self.merchant_id = merchant_id
        self.payment_link: Optional[str] = None

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
        return f"AP-{self.merchant_id}-123456"

    def send_payment_link(self, email: str) -> bool:
        print(f"Sending Apple Pay payment link to {email}")
        self.payment_link = f"https://applepay.com/pay?merchant={self.merchant_id}"
        return True

    def get_payment_link(self) -> str:
        return self.payment_link or "No payment link generated"
