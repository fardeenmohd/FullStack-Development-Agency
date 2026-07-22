import unittest
from unittest.mock import patch, MagicMock
from product_collaboration.real_time_updates import RealTimeUpdates

class TestRealTimeUpdates(unittest.TestCase):

    @patch('product_collaboration.real_time_updates.WebSocket')
    def test_real_time_updates(self, mock_websocket):
        # Arrange
        real_time_updates = RealTimeUpdates()
        mock_websocket.return_value.send_message.side_effect = lambda message: print(f"Sent message: {message}")
        
        # Act
        real_time_updates.update_data("user1", "new data")
        
        # Assert
        mock_websocket.return_value.send_message.assert_called_once_with('{"user": "user1", "data": "new data"}')

    @patch('product_collaboration.real_time_updates.WebSocket')
    def test_real_time_notifications(self, mock_websocket):
        # Arrange
        real_time_updates = RealTimeUpdates()
        mock_websocket.return_value.send_message.side_effect = lambda message: print(f"Sent message: {message}")
        
        # Act
        real_time_updates.notify_users("new data")
        
        # Assert
        mock_websocket.return_value.send_message.assert_called_once_with('{"data": "new data"}')

    @patch('product_collaboration.real_time_updates.WebSocket')
    def test_real_time_updates_multiple_users(self, mock_websocket):
        # Arrange
        real_time_updates = RealTimeUpdates()
        mock_websocket.return_value.send_message.side_effect = lambda message: print(f"Sent message: {message}")
        
        # Act
        real_time_updates.update_data("user1", "new data")
        real_time_updates.update_data("user2", "updated data")
        
        # Assert
        mock_websocket.return_value.send_message.assert_has_calls([
            MagicMock(side_effect=lambda message: print(f"Sent message: {message}")),
            MagicMock(side_effect=lambda message: print(f"Sent message: {message}"))
        ])

    @patch('product_collaboration.real_time_updates.WebSocket')
    def test_real_time_notifications_multiple_data(self, mock_websocket):
        # Arrange
        real_time_updates = RealTimeUpdates()
        mock_websocket.return_value.send_message.side_effect = lambda message: print(f"Sent message: {message}")
        
        # Act
        real_time_updates.notify_users("new data")
        real_time_updates.notify_users("updated data")
        
        # Assert
        mock_websocket.return_value.send_message.assert_has_calls([
            MagicMock(side_effect=lambda message: print(f"Sent message: {message}")),
            MagicMock(side_effect=lambda message: print(f"Sent message: {message}"))
        ])

if __name__ == '__main__':
    unittest.main()
