import unittest
from fastapi.testclient import TestClient
from main import app  # Assuming the FastAPI app is defined in a file named 'main.py'
from Task import Base, Task
from database import SessionLocal, engine

# Create the tables in the test database
Base.metadata.create_all(bind=engine)

class TestTask(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        # Create a test session
        self.db = SessionLocal()

    def tearDown(self):
        # Close the test session and drop all tables
        self.db.close()
        Base.metadata.drop_all(bind=engine)

    def test_create_task(self):
        response = self.client.post(
            "/tasks/",
            json={
                "title": "Test Task",
                "description": "This is a test task.",
                "product_id": 1,
                "user_id": 1
            }
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("id", data)
        self.assertEqual(data["title"], "Test Task")
        self.assertEqual(data["description"], "This is a test task.")
        self.assertEqual(data["product_id"], 1)
        self.assertEqual(data["user_id"], 1)

    def test_read_task(self):
        # Create a task first
        response = self.client.post(
            "/tasks/",
            json={
                "title": "Test Task",
                "description": "This is a test task.",
                "product_id": 1,
                "user_id": 1
            }
        )
        task_id = response.json()["id"]

        # Read the created task
        response = self.client.get(f"/tasks/{task_id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["id"], task_id)
        self.assertEqual(data["title"], "Test Task")
        self.assertEqual(data["description"], "This is a test task.")
        self.assertEqual(data["product_id"], 1)
        self.assertEqual(data["user_id"], 1)

    def test_update_task(self):
        # Create a task first
        response = self.client.post(
            "/tasks/",
            json={
                "title": "Test Task",
                "description": "This is a test task.",
                "product_id": 1,
                "user_id": 1
            }
        )
        task_id = response.json()["id"]

        # Update the created task
        response = self.client.put(
            f"/tasks/{task_id}",
            json={
                "title": "Updated Task",
                "description": "This is an updated test task.",
                "product_id": 2,
                "user_id": 2
            }
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["id"], task_id)
        self.assertEqual(data["title"], "Updated Task")
        self.assertEqual(data["description"], "This is an updated test task.")
        self.assertEqual(data["product_id"], 2)
        self.assertEqual(data["user_id"], 2)

    def test_delete_task(self):
        # Create a task first
        response = self.client.post(
            "/tasks/",
            json={
                "title": "Test Task",
                "description": "This is a test task.",
                "product_id": 1,
                "user_id": 1
            }
        )
        task_id = response.json()["id"]

        # Delete the created task
        response = self.client.delete(f"/tasks/{task_id}")
        self.assertEqual(response.status_code, 204)

if __name__ == "__main__":
    unittest.main()
