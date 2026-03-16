import pytest
from unittest.mock import MagicMock
from dependency_inversion.with_principle import FundsAssignationService


class TestFundsAssignationService:

    def setup_method(self):
        self.mock_database = MagicMock()
        self.mock_notification_service = MagicMock()

        self.mock_database.get_account_balance.return_value = 100000.0
        self.mock_database.save_assignation.return_value = True
        self.mock_notification_service.send_funds_assignation_notification.return_value = True

        self.service = FundsAssignationService(
            database=self.mock_database,
            notification_service=self.mock_notification_service
        )

    def test_assign_funds_successfully_when_account_has_sufficient_balance(self):

        assignation_data = {
            'from_account': 'ACC001',
            'to_account': 'ACC002',
            'amount': 5000.0,
            'client_email': 'test@example.com'
        }

        result = self.service.assign_funds(assignation_data)

        assert result['from_account'] == 'ACC001'
        assert result['to_account'] == 'ACC002'
        assert result['amount'] == 5000.0
        self.mock_database.get_account_balance.assert_called_once_with('ACC001')
        self.mock_database.save_assignation.assert_called_once()
        self.mock_notification_service.send_funds_assignation_notification.assert_called_once_with(
            recipient='test@example.com'
        )

    def test_assign_funds_fails_when_account_has_insufficient_balance(self):
        self.mock_database.get_account_balance.return_value = 1000.0

        assignation_data = {
            'from_account': 'ACC001',
            'to_account': 'ACC002',
            'amount': 5000.0,
            'client_email': 'test@example.com'
        }

        with pytest.raises(ValueError, match="Insufficient funds"):
            self.service.assign_funds(assignation_data)

        self.mock_database.get_account_balance.assert_called_once_with('ACC001')
        self.mock_database.save_assignation.assert_not_called()
        self.mock_notification_service.send_funds_assignation_notification.assert_not_called()

    def test_assign_funds_fails_when_amount_is_negative(self):

        assignation_data = {
            'from_account': 'ACC001',
            'to_account': 'ACC002',
            'amount': -100.0,
            'client_email': 'test@example.com'
        }

        with pytest.raises(ValueError, match="Amount must be positive"):
            self.service.assign_funds(assignation_data)

        self.mock_database.get_account_balance.assert_called_once_with('ACC001')
        self.mock_database.save_assignation.assert_not_called()
        self.mock_notification_service.send_funds_assignation_notification.assert_not_called()

    def test_assign_funds_fails_when_amount_exceeds_maximum_limit(self):
        self.mock_database.get_account_balance.return_value = 2000000.0

        assignation_data = {
            'from_account': 'ACC001',
            'to_account': 'ACC002',
            'amount': 1500000.0,
            'client_email': 'test@example.com'
        }

        with pytest.raises(ValueError, match="Amount exceeds maximum limit"):
            self.service.assign_funds(assignation_data)

        self.mock_database.get_account_balance.assert_called_once_with('ACC001')
        self.mock_database.save_assignation.assert_not_called()
        self.mock_notification_service.send_funds_assignation_notification.assert_not_called()

    def test_assign_funds_successfully_with_custom_currency(self):

        assignation_data = {
            'from_account': 'ACC001',
            'to_account': 'ACC002',
            'amount': 5000.0,
            'currency': 'USD',
            'client_email': 'test@example.com'
        }

        result = self.service.assign_funds(assignation_data)

        assert result['currency'] == 'USD'
        self.mock_database.get_account_balance.assert_called_once()
        self.mock_database.save_assignation.assert_called_once()
        self.mock_notification_service.send_funds_assignation_notification.assert_called_once()


