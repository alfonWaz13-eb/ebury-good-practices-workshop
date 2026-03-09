from datetime import datetime


class MySQLDatabase:

    @classmethod
    def save_assignation(cls, assignation_data):
        print(f"[MySQL] Saving assignation")
        print(f"[MySQL] Data: {assignation_data}")
        return True

    @classmethod
    def get_account_balance(cls, account_id):
        balances = {
            'ACC001': 100000.0,
            'ACC002': 50000.0,
            'ACC003': 250000.0
        }
        return balances.get(account_id, 0.0)


class EmailNotificationService:

    @classmethod
    def send_funds_assignation_notification(cls, recipient):
        print(f"[Email] Sending email to {recipient}")
        return True


class FundsAssignationService:

    def assign_funds(self, assignation_data):
        assignation = {
            'id': len(self.assignations) + 1,
            'from_account': assignation_data['from_account'],
            'to_account': assignation_data['to_account'],
            'amount': assignation_data['amount'],
            'currency': assignation_data.get('currency', 'EUR'),
            'client_email': assignation_data['client_email'],
            'reason': assignation_data.get('reason', 'Fund transfer'),
        }

        balance = MySQLDatabase.get_account_balance(assignation['from_account'])
        self._validate_amount(assignation, balance)
        MySQLDatabase.save_assignation(assignation)

        EmailNotificationService.send_funds_assignation_notification(recipient=assignation['client_email'])

        return assignation

    @staticmethod
    def _validate_amount(assignation, balance):
        if balance < assignation['amount']:
            raise ValueError(f"Insufficient funds in account {assignation['from_account']}")

        if assignation['amount'] <= 0:
            raise ValueError("Amount must be positive")

        if assignation['amount'] > 1000000:
            raise ValueError("Amount exceeds maximum limit")
