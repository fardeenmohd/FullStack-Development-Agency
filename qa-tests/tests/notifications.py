import unittest
from app import create_app, db
from models.notification import Notification

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
            'title': 'Test Notification',
            'message': 'This is a test notification.'
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('id', data)

    def test_update_notification(self):
        with self.app.app_context():
            notification = Notification(title='Old Title', message='Old Message')
            db.session.add(notification)
            db.session.commit()

        response = self.client.put(f'/notifications/{notification.id}', json={
            'title': 'Updated Title',
            'message': 'Updated Message'
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['title'], 'Updated Title')
        self.assertEqual(data['message'], 'Updated Message')

    def test_delete_notification(self):
        with self.app.app_context():
            notification = Notification(title='Test Notification', message='This is a test notification.')
            db.session.add(notification)
            db.session.commit()

        response = self.client.delete(f'/notifications/{notification.id}')
        self.assertEqual(response.status_code, 204)

    def test_delivery_mechanism(self):
        with self.app.app_context():
            notification = Notification(title='Delivery Test', message='This is a delivery test.')
            db.session.add(notification)
            db.session.commit()

        response = self.client.post('/notifications/deliver', json={
            'id': notification.id
        })
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
