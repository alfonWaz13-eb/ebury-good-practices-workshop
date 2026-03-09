import pytest
from unittest.mock import patch
from dependency_inversion.original import FundsAssignationService


class TestFundsAssignationService:

    @patch('dependency_inversion.original.EmailNotificationService.send_funds_assignation_notification')
    @patch('dependency_inversion.original.MySQLDatabase.save_assignation')
    @patch('dependency_inversion.original.MySQLDatabase.get_account_balance')
    @patch.object(FundsAssignationService, 'assignations', [])
    def test_assign_funds_successfully_when_account_has_sufficient_balance(self, mock_get_balance, mock_save, mock_send_notification):
        mock_get_balance.return_value = 100000.0
        mock_save.return_value = True
        mock_send_notification.return_value = True

        service = FundsAssignationService()
        assignation_data = {
            'from_account': 'ACC001',
            'to_account': 'ACC002',
            'amount': 5000.0,
            'client_email': 'test@example.com'
        }

        result = service.assign_funds(assignation_data)

        assert result['from_account'] == 'ACC001'
        assert result['to_account'] == 'ACC002'
        assert result['amount'] == 5000.0
        mock_get_balance.assert_called_once_with('ACC001')
        mock_save.assert_called_once()
        mock_send_notification.assert_called_once_with(recipient='test@example.com')

    @patch('dependency_inversion.original.EmailNotificationService.send_funds_assignation_notification')
    @patch('dependency_inversion.original.MySQLDatabase.save_assignation')
    @patch('dependency_inversion.original.MySQLDatabase.get_account_balance')
    @patch.object(FundsAssignationService, 'assignations', [])
    def test_assign_funds_fails_when_account_has_insufficient_balance(self, mock_get_balance, mock_save, mock_send_notification):
        mock_get_balance.return_value = 1000.0

        service = FundsAssignationService()
        assignation_data = {
            'from_account': 'ACC001',
            'to_account': 'ACC002',
            'amount': 5000.0,
            'client_email': 'test@example.com'
        }

        with pytest.raises(ValueError, match="Insufficient funds"):
            service.assign_funds(assignation_data)

        mock_get_balance.assert_called_once_with('ACC001')
        mock_save.assert_not_called()
        mock_send_notification.assert_not_called()

    @patch('dependency_inversion.original.EmailNotificationService.send_funds_assignation_notification')
    @patch('dependency_inversion.original.MySQLDatabase.save_assignation')
    @patch('dependency_inversion.original.MySQLDatabase.get_account_balance')
    @patch.object(FundsAssignationService, 'assignations', [])
    def test_assign_funds_fails_when_amount_is_negative(self, mock_get_balance, mock_save, mock_send_notification):
        mock_get_balance.return_value = 100000.0

        service = FundsAssignationService()
        assignation_data = {
            'from_account': 'ACC001',
            'to_account': 'ACC002',
            'amount': -100.0,
            'client_email': 'test@example.com'
        }

        with pytest.raises(ValueError, match="Amount must be positive"):
            service.assign_funds(assignation_data)

        mock_get_balance.assert_called_once_with('ACC001')
        mock_save.assert_not_called()
        mock_send_notification.assert_not_called()

    @patch('dependency_inversion.original.EmailNotificationService.send_funds_assignation_notification')
    @patch('dependency_inversion.original.MySQLDatabase.save_assignation')
    @patch('dependency_inversion.original.MySQLDatabase.get_account_balance')
    @patch.object(FundsAssignationService, 'assignations', [])
    def test_assign_funds_fails_when_amount_exceeds_maximum_limit(self, mock_get_balance, mock_save, mock_send_notification):
        mock_get_balance.return_value = 2000000.0

        service = FundsAssignationService()
        assignation_data = {
            'from_account': 'ACC001',
            'to_account': 'ACC002',
            'amount': 1500000.0,
            'client_email': 'test@example.com'
        }

        with pytest.raises(ValueError, match="Amount exceeds maximum limit"):
            service.assign_funds(assignation_data)

        mock_get_balance.assert_called_once_with('ACC001')
        mock_save.assert_not_called()
        mock_send_notification.assert_not_called()




