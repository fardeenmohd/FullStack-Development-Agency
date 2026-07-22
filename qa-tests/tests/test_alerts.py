import unittest
from app import create_app, db
from models.alerts import Alert

class TestAlertsAPI(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_alert(self):
        response = self.client.post('/api/v1/alerts', json={
            'name': 'Test Alert',
            'criteria': {'type': 'threshold', 'value': 50}
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('id', data)

    def test_create_alert_with_invalid_criteria(self):
        response = self.client.post('/api/v1/alerts', json={
            'name': 'Test Alert',
            'criteria': {'type': 'invalid'}
        })
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

    def test_update_alert(self):
        alert = Alert(name='Old Alert', criteria={'type': 'threshold', 'value': 50})
        with self.app.app_context():
            db.session.add(alert)
            db.session.commit()

        response = self.client.put('/api/v1/alerts/1', json={
            'name': 'Updated Alert',
            'criteria': {'type': 'threshold', 'value': 60}
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('id', data)
        self.assertEqual(data['name'], 'Updated Alert')
        self.assertEqual(data['criteria']['value'], 60)

    def test_update_nonexistent_alert(self):
        response = self.client.put('/api/v1/alerts/999', json={
            'name': 'Nonexistent Alert',
            'criteria': {'type': 'threshold', 'value': 50}
        })
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertIn('error', data)

    def test_delete_alert(self):
        alert = Alert(name='Test Alert', criteria={'type': 'threshold', 'value': 50})
        with self.app.app_context():
            db.session.add(alert)
            db.session.commit()

        response = self.client.delete('/api/v1/alerts/1')
        self.assertEqual(response.status_code, 204)

    def test_delete_nonexistent_alert(self):
        response = self.client.delete('/api/v1/alerts/999')
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertIn('error', data)

if __name__ == '__main__':
    unittest.main()
