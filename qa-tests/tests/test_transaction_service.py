import unittest
from unittest.mock import patch
from services.transaction_service import TransactionService

class TestTransactionService(unittest.TestCase):

    @patch('services.transaction_service.send_notification')
    def test_trigger_notification_on_status_change(self, mock_send_notification):
        # Arrange
        service = TransactionService()
        transaction_id = '12345'
        old_status = 'pending'
        new_status = 'completed'

        # Act
        service.trigger_notification(transaction_id, old_status, new_status)

        # Assert
        mock_send_notification.assert_called_once_with(transaction_id, new_status)

if __name__ == '__main__':
    unittest.main()
