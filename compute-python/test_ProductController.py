import unittest
from fastapi.testclient import TestClient
from ProductController import app

class TestProductController(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_login(self):
        response = self.client.post('/login', json={'username': 'admin', 'password': 'password'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.json())

        response = self.client.post('/login', json={'username': 'admin', 'password': 'wrong_password'})
        self.assertEqual(response.status_code, 401)

    def test_get_products(self):
        access_token = self.get_access_token()
        headers = {'Authorization': f'Bearer {access_token}'}
        response = self.client.get('/products', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_update_product(self):
        access_token = self.get_access_token()
        headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}
        response = self.client.put('/products/1', headers=headers, json={'status': 'completed'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'completed')

    def test_create_task(self):
        access_token = self.get_access_token()
        headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}
        response = self.client.post('/tasks', headers=headers, json={'name': 'Task 1'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('id', response.json())

    def test_update_task(self):
        access_token = self.get_access_token()
        headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}
        task_id = max([t['id'] for t in tasks] or [0]) + 1
        response = self.client.put(f'/tasks/{task_id}', headers=headers, json={'name': 'Updated Task'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], 'Updated Task')

    def test_update_task_progress(self):
        access_token = self.get_access_token()
        headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}
        task_id = max([t['id'] for t in tasks] or [0]) + 1
        response = self.client.put(f'/tasks/{task_id}/progress', headers=headers, json={'progress': 50})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['progress'], 50)

    def test_assign_task_to_product(self):
        access_token = self.get_access_token()
        headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}
        response = self.client.post('/products/1/assign_task', headers=headers, json={'name': 'Task 1'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('assigned_task', response.json())

    def test_unassign_task_from_product(self):
        access_token = self.get_access_token()
        headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}
        response = self.client.post('/products/1/unassign_task', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('assigned_task', response.json())

    def test_real_time_update_product(self):
        access_token = self.get_access_token()
        headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}
        response = self.client.put('/products/1/real_time_update', headers=headers, json={'status': 'pending'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'pending')

    def get_access_token(self):
        response = self.client.post('/login', json={'username': 'admin', 'password': 'password'})
        return response.json().get('access_token')

if __name__ == '__main__':
    unittest.main()
