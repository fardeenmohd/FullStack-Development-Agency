import unittest
from compute.api import TasksAPI

class TestTasksAPI(unittest.TestCase):
    def setUp(self):
        self.tasks_api = TasksAPI()

    def test_task_operations_success(self):
        task_data = {
            "name": "Test Task",
            "description": "This is a test task.",
            "due_date": "2023-12-31"
        }
        response_create = self.tasks_api.create_task(task_data)
        self.assertEqual(response_create["status"], "success")
        self.assertIn("task_id", response_create)

        task_id = response_create["task_id"]
        response_get = self.tasks_api.get_task(task_id)
        self.assertEqual(response_get["status"], "success")
        self.assertIn("task", response_get)

        update_data = {
            "name": "Updated Task",
            "description": "This is an updated task.",
            "due_date": "2024-01-31"
        }
        response_update = self.tasks_api.update_task(task_id, update_data)
        self.assertEqual(response_update["status"], "success")
        self.assertIn("task", response_update)

        response_delete = self.tasks_api.delete_task(task_id)
        self.assertEqual(response_delete["status"], "success")

    def test_task_operations_failure(self):
        task_data = {
            "name": "",
            "description": "This is a test task.",
            "due_date": "2023-12-31"
        }
        response_create = self.tasks_api.create_task(task_data)
        self.assertEqual(response_create["status"], "error")
        self.assertIn("message", response_create)

        task_id = 999
        response_get = self.tasks_api.get_task(task_id)
        self.assertEqual(response_get["status"], "error")
        self.assertIn("message", response_get)

        update_data = {
            "name": "Updated Task",
            "description": "This is an updated task.",
            "due_date": "2024-01-31"
        }
        response_update = self.tasks_api.update_task(task_id, update_data)
        self.assertEqual(response_update["status"], "error")
        self.assertIn("message", response_update)

        response_delete = self.tasks_api.delete_task(task_id)
        self.assertEqual(response_delete["status"], "error")
        self.assertIn("message", response_delete)

if __name__ == "__main__":
    unittest.main()
