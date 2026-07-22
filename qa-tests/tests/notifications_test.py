import unittest
from app import create_app, db
from models import User, NotificationSubscription

class NotificationsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_subscribe_successfully(self):
        user = User(username='testuser', email='test@example.com')
        db.session.add(user)
        db.session.commit()

        response = self.client.post('/notifications/subscribe', json={'user_id': user.id, 'topic': 'news'})
        data = response.get_json()

        self.assertEqual(response.status_code, 201)
        self.assertIn('subscription', data)
        self.assertEqual(data['subscription']['user_id'], user.id)
        self.assertEqual(data['subscription']['topic'], 'news')

    def test_subscribe_with_invalid_user(self):
        response = self.client.post('/notifications/subscribe', json={'user_id': 999, 'topic': 'news'})
        data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertIn('error', data)

    def test_subscribe_with_existing_subscription(self):
        user = User(username='testuser', email='test@example.com')
        subscription = NotificationSubscription(user_id=user.id, topic='news')
        db.session.add(user)
        db.session.add(subscription)
        db.session.commit()

        response = self.client.post('/notifications/subscribe', json={'user_id': user.id, 'topic': 'news'})
        data = response.get_json()

        self.assertEqual(response.status_code, 409)
        self.assertIn('error', data)

    def test_unsubscribe_successfully(self):
        user = User(username='testuser', email='test@example.com')
        subscription = NotificationSubscription(user_id=user.id, topic='news')
        db.session.add(user)
        db.session.add(subscription)
        db.session.commit()

        response = self.client.post('/notifications/unsubscribe', json={'user_id': user.id, 'topic': 'news'})
        data = response.get_json()

        self.assertEqual(response.status_code, 204)

    def test_unsubscribe_with_invalid_user(self):
        response = self.client.post('/notifications/unsubscribe', json={'user_id': 999, 'topic': 'news'})
        data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertIn('error', data)

    def test_unsubscribe_with_non_existent_subscription(self):
        user = User(username='testuser', email='test@example.com')
        db.session.add(user)
        db.session.commit()

        response = self.client.post('/notifications/unsubscribe', json={'user_id': user.id, 'topic': 'news'})
        data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertIn('error', data)

if __name__ == '__main__':
    unittest.main()
