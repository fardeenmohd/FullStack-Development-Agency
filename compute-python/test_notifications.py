import unittest
from fastapi.testclient import TestClient
from notifications import app, db, UserSubscription, validate_subscription_data

class NotificationsTestCase(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_validate_subscription_data_valid(self):
        data = {
            "event_type": "new_lead",
            "notification_method": "email"
        }
        is_valid, error_message, status_code = validate_subscription_data(data)
        self.assertTrue(is_valid)
        self.assertIsNone(error_message)
        self.assertEqual(status_code, 200)

    def test_validate_subscription_data_missing_field(self):
        data = {
            "event_type": "new_lead"
        }
        is_valid, error_message, status_code = validate_subscription_data(data)
        self.assertFalse(is_valid)
        self.assertIn('Missing required fields', error_message['message'])
        self.assertEqual(status_code, 400)

    def test_validate_subscription_data_invalid_event_type(self):
        data = {
            "event_type": "invalid_event",
            "notification_method": "email"
        }
        is_valid, error_message, status_code = validate_subscription_data(data)
        self.assertFalse(is_valid)
        self.assertIn('Invalid event type', error_message['message'])
        self.assertEqual(status_code, 400)

    def test_validate_subscription_data_invalid_notification_method(self):
        data = {
            "event_type": "new_lead",
            "notification_method": "invalid_method"
        }
        is_valid, error_message, status_code = validate_subscription_data(data)
        self.assertFalse(is_valid)
        self.assertIn('Invalid notification method', error_message['message'])
        self.assertEqual(status_code, 400)

    def test_subscribe_success(self):
        headers = {
            'Authorization': 'Bearer fake_token'
        }
        data = {
            "event_type": "new_lead",
            "notification_method": "email"
        }
        response = self.client.post('/subscribe', json=data, headers=headers)
        self.assertEqual(response.status_code, 201)
        self.assertIn('Subscription successful', response.json['message'])

    def test_subscribe_invalid_token(self):
        data = {
            "event_type": "new_lead",
            "notification_method": "email"
        }
        response = self.client.post('/subscribe', json=data)
        self.assertEqual(response.status_code, 401)

    def test_get_subscriptions_success(self):
        headers = {
            'Authorization': 'Bearer fake_token'
        }
        data = {
            "event_type": "new_lead",
            "notification_method": "email"
        }
        self.client.post('/subscribe', json=data, headers=headers)
        response = self.client.get('/subscriptions', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('new_lead', response.json[0]['event_type'])

    def test_get_subscriptions_invalid_token(self):
        response = self.client.get('/subscriptions')
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main()
