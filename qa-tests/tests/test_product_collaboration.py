import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_comment():
    response = client.post("/products/1/comments", json={"text": "Great product!"})
    assert response.status_code == 201
    assert response.json()["text"] == "Great product!"

def test_assign_task():
    response = client.post("/products/1/tasks", json={"assignee_id": 2, "description": "Review the design"})
    assert response.status_code == 201
    assert response.json()["assignee_id"] == 2

def test_update_progress():
    response = client.put("/products/1/progress", json={"status": "In Progress"})
    assert response.status_code == 200
    assert response.json()["status"] == "In Progress"

def test_get_comments():
    response = client.get("/products/1/comments")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_get_tasks():
    response = client.get("/products/1/tasks")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_get_progress():
    response = client.get("/products/1/progress")
    assert response.status_code == 200
    assert "status" in response.json()

def test_delete_comment():
    comment_response = client.post("/products/1/comments", json={"text": "Great product!"})
    comment_id = comment_response.json()["id"]
    delete_response = client.delete(f"/products/1/comments/{comment_id}")
    assert delete_response.status_code == 204

def test_update_task():
    task_response = client.post("/products/1/tasks", json={"assignee_id": 2, "description": "Review the design"})
    task_id = task_response.json()["id"]
    update_response = client.put(f"/products/1/tasks/{task_id}", json={"assignee_id": 3, "description": "Update the design"})
    assert update_response.status_code == 200
    assert update_response.json()["assignee_id"] == 3

def test_delete_task():
    task_response = client.post("/products/1/tasks", json={"assignee_id": 2, "description": "Review the design"})
    task_id = task_response.json()["id"]
    delete_response = client.delete(f"/products/1/tasks/{task_id}")
    assert delete_response.status_code == 204

def test_get_specific_comment():
    comment_response = client.post("/products/1/comments", json={"text": "Great product!"})
    comment_id = comment_response.json()["id"]
    get_response = client.get(f"/products/1/comments/{comment_id}")
    assert get_response.status_code == 200
    assert get_response.json()["text"] == "Great product!"

def test_get_specific_task():
    task_response = client.post("/products/1/tasks", json={"assignee_id": 2, "description": "Review the design"})
    task_id = task_response.json()["id"]
    get_response = client.get(f"/products/1/tasks/{task_id}")
    assert get_response.status_code == 200
    assert get_response.json()["description"] == "Review the design"
