import unittest
from app import create_app, db
from models.notification import Notification, Subscription

class TestNotificationAPI(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_notification(self):
        response = self.client.post('/notifications', json={
            'user_id': 1,
            'event_type': 'new_post',
            'data': {'post_id': 1}
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('id', data)

    def test_update_notification(self):
        notification = Notification(user_id=1, event_type='new_post', data={'post_id': 1})
        db.session.add(notification)
        db.session.commit()

        response = self.client.put(f'/notifications/{notification.id}', json={
            'user_id': 2,
            'event_type': 'comment',
            'data': {'comment_id': 1}
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['user_id'], 2)
        self.assertEqual(data['event_type'], 'comment')
        self.assertEqual(data['data']['comment_id'], 1)

    def test_delete_notification(self):
        notification = Notification(user_id=1, event_type='new_post', data={'post_id': 1})
        db.session.add(notification)
        db.session.commit()

        response = self.client.delete(f'/notifications/{notification.id}')
        self.assertEqual(response.status_code, 204)

    def test_create_notification_missing_fields(self):
        response = self.client.post('/notifications', json={
            'user_id': 1,
            'event_type': 'new_post'
        })
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('message', data)

    def test_update_notification_nonexistent_id(self):
        response = self.client.put('/notifications/999', json={
            'user_id': 2,
            'event_type': 'comment',
            'data': {'comment_id': 1}
        })
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertIn('message', data)

    def test_delete_notification_nonexistent_id(self):
        response = self.client.delete('/notifications/999')
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertIn('message', data)

class TestNotificationDelivery(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_deliver_notification(self):
        subscription = Subscription(user_id=1, event_type='new_post')
        db.session.add(subscription)
        db.session.commit()

        response = self.client.post('/notifications/trigger', json={
            'event_type': 'new_post',
            'data': {'post_id': 1}
        })
        self.assertEqual(response.status_code, 200)

    def test_deliver_notification_no_subscriptions(self):
        response = self.client.post('/notifications/trigger', json={
            'event_type': 'new_post',
            'data': {'post_id': 1}
        })
        self.assertEqual(response.status_code, 204)

    def test_deliver_notification_invalid_event(self):
        response = self.client.post('/notifications/trigger', json={
            'event_type': 'invalid_event',
            'data': {'post_id': 1}
        })
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('message', data)

    def test_deliver_notification_failed_api_call(self):
        subscription = Subscription(user_id=1, event_type='new_post')
        db.session.add(subscription)
        db.session.commit()

        response = self.client.post('/notifications/trigger', json={
            'event_type': 'new_post',
            'data': {'post_id': 1}
        }, headers={'X-Fail-API-Call': 'true'})
        self.assertEqual(response.status_code, 500)

class TestNotificationModel(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_notification_creation(self):
        notification = Notification(user_id=1, event_type='new_post', data={'post_id': 1})
        self.assertEqual(notification.user_id, 1)
        self.assertEqual(notification.event_type, 'new_post')
        self.assertEqual(notification.data, {'post_id': 1})

class TestSubscriptionModel(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_subscription_creation(self):
        subscription = Subscription(user_id=1, event_type='new_post')
        self.assertEqual(subscription.user_id, 1)
        self.assertEqual(subscription.event_type, 'new_post')

class TestNotificationFrontend(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_notification_display(self):
        notification = Notification(user_id=1, event_type='new_post', data={'post_id': 1})
        response = self.client.get(f'/notifications/{notification.id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['user_id'], 1)
        self.assertEqual(data['event_type'], 'new_post')
        self.assertEqual(data['data']['post_id'], 1)

    def test_notification_display_nonexistent_id(self):
        response = self.client.get('/notifications/999')
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertIn('message', data)

if __name__ == '__main__':
    unittest.main()
