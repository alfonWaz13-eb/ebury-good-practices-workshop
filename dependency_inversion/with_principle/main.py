from dependency_inversion.with_principle.notification import NotificationService
from dependency_inversion.with_principle.repository import DatabaseRepository


class FundsAssignationService:

    def __init__(
            self,
            database: DatabaseRepository,
            notification_service: NotificationService
    ):
        self.database = database
        self.notification_service = notification_service

    def assign_funds(self, assignation_data):
        assignation = {
            'from_account': assignation_data['from_account'],
            'to_account': assignation_data['to_account'],
            'amount': assignation_data['amount'],
            'currency': assignation_data.get('currency', 'EUR'),
            'client_email': assignation_data['client_email'],
            'reason': assignation_data.get('reason', 'Fund transfer'),
        }

        balance = self.database.get_account_balance(assignation['from_account'])
        self._validate_amount(assignation, balance)
        self.database.save_assignation(assignation)

        self.notification_service.send_funds_assignation_notification(recipient=assignation['client_email'])

        return assignation

    @staticmethod
    def _validate_amount(assignation, balance):
        if balance < assignation['amount']:
            raise ValueError(f"Insufficient funds in account {assignation['from_account']}")

        if assignation['amount'] <= 0:
            raise ValueError("Amount must be positive")

        if assignation['amount'] > 1000000:
            raise ValueError("Amount exceeds maximum limit")
