from unittest.mock import patch, MagicMock
import pytest
from api.notifications import subscribe_user_to_event, trigger_notification_event

# Mock data for testing
MOCK_USER_ID = "user123"
MOCK_EVENT_TYPE = "new_message"

def test_subscribe_user_to_event_valid_input():
    with patch('api.notifications.database.add_subscription') as mock_add:
        result = subscribe_user_to_event(MOCK_USER_ID, MOCK_EVENT_TYPE)
        assert result == True
        mock_add.assert_called_once_with(MOCK_USER_ID, MOCK_EVENT_TYPE)

def test_subscribe_user_to_event_invalid_user_id():
    with patch('api.notifications.database.add_subscription') as mock_add:
        result = subscribe_user_to_event(None, MOCK_EVENT_TYPE)
        assert result == False
        mock_add.assert_not_called()

def test_subscribe_user_to_event_unsupported_event_type():
    with patch('api.notifications.database.add_subscription') as mock_add:
        result = subscribe_user_to_event(MOCK_USER_ID, "unsupported_event")
        assert result == False
        mock_add.assert_not_called()

def test_trigger_notification_event_valid_input():
    with patch('api.notifications.database.get_subscriptions_by_event_type') as mock_get_subs, \
         patch('api.notifications.send_notification') as mock_send:
        mock_get_subs.return_value = [{"user_id": "user123"}, {"user_id": "user456"}]
        result = trigger_notification_event(MOCK_EVENT_TYPE, "message content")
        assert result == True
        mock_get_subs.assert_called_once_with(MOCK_EVENT_TYPE)
        mock_send.assert_has_calls([
            MagicMock(user_id="user123", event_type=MOCK_EVENT_TYPE, message="message content"),
            MagicMock(user_id="user456", event_type=MOCK_EVENT_TYPE, message="message content")
        ])

def test_trigger_notification_event_no_subscriptions():
    with patch('api.notifications.database.get_subscriptions_by_event_type') as mock_get_subs:
        mock_get_subs.return_value = []
        result = trigger_notification_event(MOCK_EVENT_TYPE, "message content")
        assert result == False
        mock_get_subs.assert_called_once_with(MOCK_EVENT_TYPE)

def test_trigger_notification_event_empty_message():
    with patch('api.notifications.database.get_subscriptions_by_event_type') as mock_get_subs:
        mock_get_subs.return_value = [{"user_id": "user123"}, {"user_id": "user456"}]
        result = trigger_notification_event(MOCK_EVENT_TYPE, "")
        assert result == False
        mock_get_subs.assert_not_called()

def test_trigger_notification_event_invalid_event_type():
    with patch('api.notifications.database.get_subscriptions_by_event_type') as mock_get_subs:
        mock_get_subs.return_value = [{"user_id": "user123"}, {"user_id": "user456"}]
        result = trigger_notification_event("unsupported_event", "message content")
        assert result == False
        mock_get_subs.assert_not_called()

def test_trigger_notification_event_no_subscriptions_for_event_type():
    with patch('api.notifications.database.get_subscriptions_by_event_type') as mock_get_subs:
        mock_get_subs.return_value = []
        result = trigger_notification_event(MOCK_EVENT_TYPE, "message content")
        assert result == False
        mock_get_subs.assert_called_once_with(MOCK_EVENT_TYPE)

def test_subscribe_user_to_event_duplicate_subscription():
    with patch('api.notifications.database.add_subscription') as mock_add:
        mock_add.side_effect = [True, False]  # First call adds subscription, second fails due to duplicate
        result1 = subscribe_user_to_event(MOCK_USER_ID, MOCK_EVENT_TYPE)
        result2 = subscribe_user_to_event(MOCK_USER_ID, MOCK_EVENT_TYPE)
        assert result1 == True
        assert result2 == False
        mock_add.assert_has_calls([
            MagicMock(user_id=MOCK_USER_ID, event_type=MOCK_EVENT_TYPE),
            MagicMock(user_id=MOCK_USER_ID, event_type=MOCK_EVENT_TYPE)
        ])
