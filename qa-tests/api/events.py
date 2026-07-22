import unittest
from unittest.mock import patch, MagicMock
from api.events import trigger_notifications

class TestTriggerNotifications(unittest.TestCase):

    @patch('api.notifications.send_email')
    @patch('api.notifications.send_sms')
    def test_trigger_notifications(self, mock_send_sms, mock_send_email):
        event_data = {
            'type': 'email',
            'recipient': 'test@example.com',
            'message': 'Hello, this is a test email.'
        }
        trigger_notifications(event_data)
        if event_data['type'] == 'email':
            mock_send_email.assert_called_once_with(event_data['recipient'], event_data['message'])
            mock_send_sms.assert_not_called()
        elif event_data['type'] == 'sms':
            mock_send_sms.assert_called_once_with(event_data['recipient'], event_data['message'])
            mock_send_email.assert_not_called()
        else:
            mock_send_sms.assert_not_called()
            mock_send_email.assert_not_called()

    @patch('api.notifications.send_email')
    @patch('api.notifications.send_sms')
    def test_trigger_notifications_invalid_type(self, mock_send_sms, mock_send_email):
        event_data = {
            'type': 'invalid',
            'recipient': '+1234567890',
            'message': 'Hello, this is a test message.'
        }
        trigger_notifications(event_data)
        mock_send_sms.assert_not_called()
        mock_send_email.assert_not_called()

if __name__ == '__main__':
    unittest.main()
