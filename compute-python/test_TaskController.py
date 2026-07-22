import unittest
from fastapi.testclient import TestClient
from main import app, tasks, users  # Assuming the file is named `main.py`

class TaskControllerTestCase(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        tasks.clear()
        users.clear()

    def test_login_success(self):
        response = self.client.post('/login', json={'username': 'admin', 'password': 'password'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.json())

    def test_login_failure(self):
        response = self.client.post('/login', json={'username': 'admin', 'password': 'wrong_password'})
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"msg": "Bad username or password"})

    def test_assign_task_success(self):
        login_response = self.client.post('/login', json={'username': 'admin', 'password': 'password'})
        access_token = login_response.json()['access_token']
        headers = {'Authorization': f'Bearer {access_token}'}
        response = self.client.post(
            '/tasks',
            json={'task_id': '123', 'user_id': 'user1'},
            headers=headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"msg": "Task assigned successfully"})
        self.assertIn('123', tasks)

    def test_assign_task_missing_data(self):
        login_response = self.client.post('/login', json={'username': 'admin', 'password': 'password'})
        access_token = login_response.json()['access_token']
        headers = {'Authorization': f'Bearer {access_token}'}
        response = self.client.post(
            '/tasks',
            json={'task_id': '123'},
            headers=headers
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"msg": "Missing data"})

    def test_assign_task_user_not_found(self):
        login_response = self.client.post('/login', json={'username': 'admin', 'password': 'password'})
        access_token = login_response.json()['access_token']
        headers = {'Authorization': f'Bearer {access_token}'}
        response = self.client.post(
            '/tasks',
            json={'task_id': '123', 'user_id': 'nonexistent_user'},
            headers=headers
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"msg": "User not found"})

    def test_update_task_success(self):
        login_response = self.client.post('/login', json={'username': 'admin', 'password': 'password'})
        access_token = login_response.json()['access_token']
        headers = {'Authorization': f'Bearer {access_token}'}
        self.client.post(
            '/tasks',
            json={'task_id': '123', 'user_id': 'user1'},
            headers=headers
        )
        response = self.client.put(
            '/tasks/123',
            json={'status': 'completed'},
            headers=headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"msg": "Task updated successfully"})
        self.assertEqual(tasks['123']['status'], 'completed')

    def test_update_task_missing_data(self):
        login_response = self.client.post('/login', json={'username': 'admin', 'password': 'password'})
        access_token = login_response.json()['access_token']
        headers = {'Authorization': f'Bearer {access_token}'}
        response = self.client.put(
            '/tasks/123',
            json={},
            headers=headers
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"msg": "Missing data"})

    def test_update_task_task_not_found(self):
        login_response = self.client.post('/login', json={'username': 'admin', 'password': 'password'})
        access_token = login_response.json()['access_token']
        headers = {'Authorization': f'Bearer {access_token}'}
        response = self.client.put(
            '/tasks/456',
            json={'status': 'completed'},
            headers=headers
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"msg": "Task not found"})

    def test_update_task_unauthorized(self):
        login_response = self.client.post('/login', json={'username': 'user1', 'password': 'password'})
        access_token = login_response.json()['access_token']
        headers = {'Authorization': f'Bearer {access_token}'}
        self.client.post(
            '/tasks',
            json={'task_id': '123', 'user_id': 'user1'},
            headers=headers
        )
        response = self.client.put(
            '/tasks/123',
            json={'status': 'completed'},
            headers=headers
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {"msg": "Unauthorized"})

    def test_notify_task_success(self):
        login_response = self.client.post('/login', json={'username': 'admin', 'password': 'password'})
        access_token = login_response.json()['access_token']
        headers = {'Authorization': f'Bearer {access_token}'}
        self.client.post(
            '/tasks',
            json={'task_id': '123', 'user_id': 'user1'},
            headers=headers
        )
        response = self.client.post(
            '/tasks/123/notify',
            headers=headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"msg": "Notification sent successfully"})

    def test_notify_task_missing_data(self):
        login_response = self.client.post('/login', json={'username': 'admin', 'password': 'password'})
        access_token = login_response.json()['access_token']
        headers = {'Authorization': f'Bearer {access_token}'}
        response = self.client.post(
            '/tasks/123/notify',
            headers=headers
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"msg": "Missing data"})

    def test_notify_task_task_not_found(self):
        login_response = self.client.post('/login', json={'username': 'admin', 'password': 'password'})
        access_token = login_response.json()['access_token']
        headers = {'Authorization': f'Bearer {access_token}'}
        response = self.client.post(
            '/tasks/456/notify',
            headers=headers
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"msg": "Task not found"})

    def test_notify_task_unauthorized(self):
        login_response = self.client.post('/login', json={'username': 'user1', 'password': 'password'})
        access_token = login_response.json()['access_token']
        headers = {'Authorization': f'Bearer {access_token}'}
        self.client.post(
            '/tasks',
            json={'task_id': '123', 'user_id': 'user1'},
            headers=headers
        )
        response = self.client.post(
            '/tasks/123/notify',
            headers=headers
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {"msg": "Unauthorized"})

if __name__ == '__main__':
    unittest.main()
