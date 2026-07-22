import unittest
from app import create_app, db
from models import Lead

class TestLeadPipeline(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_lead(self):
        response = self.client.post('/leads', json={'name': 'John Doe', 'email': 'john@example.com'})
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('id', data)

    def test_get_leads(self):
        with self.app.app_context():
            lead = Lead(name='Jane Doe', email='jane@example.com')
            db.session.add(lead)
            db.session.commit()

        response = self.client.get('/leads')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('id', data[0])
        self.assertEqual(data[0]['name'], 'Jane Doe')

    def test_update_lead(self):
        with self.app.app_context():
            lead = Lead(name='Jim Beam', email='jim@example.com')
            db.session.add(lead)
            db.session.commit()

        response = self.client.put(f'/leads/{lead.id}', json={'name': 'Jimmy Beam'})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['name'], 'Jimmy Beam')

    def test_delete_lead(self):
        with self.app.app_context():
            lead = Lead(name='Joe Doe', email='joe@example.com')
            db.session.add(lead)
            db.session.commit()

        response = self.client.delete(f'/leads/{lead.id}')
        self.assertEqual(response.status_code, 204)

    def test_lead_validation(self):
        response = self.client.post('/leads', json={'name': '', 'email': ''})
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

if __name__ == '__main__':
    unittest.main()
