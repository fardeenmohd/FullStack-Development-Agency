import unittest
from fastapi.testclient import TestClient
from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

# Assuming the existence of a FastAPI application and routes for Product
from main import app  # Replace 'main' with the actual module name where your FastAPI app is defined

class Comment(BaseModel):
    id: int
    content: str
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime]

class TaskAssignment(BaseModel):
    id: int
    user_id: int
    status: str
    assigned_at: datetime
    completed_at: Optional[datetime]

class Progress(BaseModel):
    id: int
    percentage_complete: float
    last_updated: datetime

class Product(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    comments: List[Comment]
    task_assignments: List[TaskAssignment]
    progress: Progress
    created_by_id: int
    updated_by_id: Optional[int]
    created_at: datetime
    updated_at: Optional[datetime]

class TestProductAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_create_product(self):
        product_data = {
            "name": "Test Product",
            "description": "This is a test product.",
            "comments": [
                {"content": "Comment 1", "user_id": 1, "created_at": datetime.utcnow()},
                {"content": "Comment 2", "user_id": 2, "created_at": datetime.utcnow()}
            ],
            "task_assignments": [
                {"user_id": 3, "status": "assigned", "assigned_at": datetime.utcnow()},
                {"user_id": 4, "status": "completed", "assigned_at": datetime.utcnow(), "completed_at": datetime.utcnow()}
            ],
            "progress": {
                "percentage_complete": 50.0,
                "last_updated": datetime.utcnow()
            },
            "created_by_id": 1
        }
        response = self.client.post("/products/", json=product_data)
        self.assertEqual(response.status_code, 200)
        created_product = response.json()
        self.assertIn("id", created_product)
        self.assertEqual(created_product["name"], product_data["name"])
        self.assertEqual(created_product["description"], product_data["description"])

    def test_get_product(self):
        # Assuming there is a product with id=1 for testing
        response = self.client.get("/products/1")
        self.assertEqual(response.status_code, 200)
        product = response.json()
        self.assertIn("id", product)
        self.assertEqual(product["name"], "Test Product")

    def test_update_product(self):
        # Assuming there is a product with id=1 for testing
        update_data = {
            "name": "Updated Test Product",
            "description": "This is an updated test product."
        }
        response = self.client.put("/products/1", json=update_data)
        self.assertEqual(response.status_code, 200)
        updated_product = response.json()
        self.assertIn("id", updated_product)
        self.assertEqual(updated_product["name"], update_data["name"])
        self.assertEqual(updated_product["description"], update_data["description"])

    def test_delete_product(self):
        # Assuming there is a product with id=1 for testing
        response = self.client.delete("/products/1")
        self.assertEqual(response.status_code, 204)

if __name__ == "__main__":
    unittest.main()
