import unittest
from fastapi.testclient import TestClient
from main import router  # Assuming the router is imported from a file named 'main.py'

class TestTaskService(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(router)

    def test_create_task(self):
        task_data = {
            "title": "Test Task",
            "description": "This is a test task.",
            "assigned_to": 1,
            "progress": 0.5
        }
        response = self.client.post("/tasks/", json=task_data)
        self.assertEqual(response.status_code, 200)
        created_task = response.json()
        self.assertEqual(created_task["title"], task_data["title"])
        self.assertEqual(created_task["description"], task_data["description"])
        self.assertEqual(created_task["assigned_to"], task_data["assigned_to"])
        self.assertEqual(created_task["progress"], task_data["progress"])

    def test_read_tasks(self):
        response = self.client.get("/tasks/")
        self.assertEqual(response.status_code, 200)
        tasks = response.json()
        self.assertIsInstance(tasks, list)

    def test_read_task(self):
        task_data = {
            "title": "Test Task",
            "description": "This is a test task.",
            "assigned_to": 1,
            "progress": 0.5
        }
        create_response = self.client.post("/tasks/", json=task_data)
        created_task = create_response.json()
        task_id = created_task["id"]
        response = self.client.get(f"/tasks/{task_id}")
        self.assertEqual(response.status_code, 200)
        read_task = response.json()
        self.assertEqual(read_task["id"], task_id)

    def test_update_task(self):
        task_data = {
            "title": "Test Task",
            "description": "This is a test task.",
            "assigned_to": 1,
            "progress": 0.5
        }
        create_response = self.client.post("/tasks/", json=task_data)
        created_task = create_response.json()
        task_id = created_task["id"]
        update_data = {
            "title": "Updated Task",
            "description": "This is an updated test task.",
            "assigned_to": 2,
            "progress": 0.75
        }
        response = self.client.put(f"/tasks/{task_id}", json=update_data)
        self.assertEqual(response.status_code, 200)
        updated_task = response.json()
        self.assertEqual(updated_task["id"], task_id)
        self.assertEqual(updated_task["title"], update_data["title"])
        self.assertEqual(updated_task["description"], update_data["description"])
        self.assertEqual(updated_task["assigned_to"], update_data["assigned_to"])
        self.assertEqual(updated_task["progress"], update_data["progress"])

    def test_delete_task(self):
        task_data = {
            "title": "Test Task",
            "description": "This is a test task.",
            "assigned_to": 1,
            "progress": 0.5
        }
        create_response = self.client.post("/tasks/", json=task_data)
        created_task = create_response.json()
        task_id = created_task["id"]
        response = self.client.delete(f"/tasks/{task_id}")
        self.assertEqual(response.status_code, 200)
        deleted_task = response.json()
        self.assertEqual(deleted_task["id"], task_id)

    def test_update_task_progress(self):
        task_data = {
            "title": "Test Task",
            "description": "This is a test task.",
            "assigned_to": 1,
            "progress": 0.5
        }
        create_response = self.client.post("/tasks/", json=task_data)
        created_task = create_response.json()
        task_id = created_task["id"]
        response = self.client.post(f"/tasks/{task_id}/update_progress/", json={"progress": 75.0})
        self.assertEqual(response.status_code, 200)
        updated_task = response.json()
        self.assertEqual(updated_task["message"], "Progress updated successfully")

    def test_assign_task(self):
        task_data = {
            "title": "Test Task",
            "description": "This is a test task.",
            "assigned_to": 1,
            "progress": 0.5
        }
        create_response = self.client.post("/tasks/", json=task_data)
        created_task = create_response.json()
        task_id = created_task["id"]
        response = self.client.post(f"/tasks/{task_id}/assign/", json={"user_id": 2})
        self.assertEqual(response.status_code, 200)
        assigned_task = response.json()
        self.assertEqual(assigned_task["message"], "Task assigned successfully")

    def test_notify_task(self):
        task_data = {
            "title": "Test Task",
            "description": "This is a test task.",
            "assigned_to": 1,
            "progress": 0.5
        }
        create_response = self.client.post("/tasks/", json=task_data)
        created_task = create_response.json()
        task_id = created_task["id"]
        response = self.client.post(f"/tasks/{task_id}/notify/")
        self.assertEqual(response.status_code, 200)
        notified_task = response.json()
        self.assertEqual(notified_task["message"], "Notification sent successfully")

if __name__ == "__main__":
    unittest.main()
