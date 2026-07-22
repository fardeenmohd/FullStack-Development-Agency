from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    assigned_to: Optional[int] = None
    progress: float = 0.0

tasks_db = []

@router.post("/tasks/", response_model=Task)
def create_task(task: Task):
    task.id = len(tasks_db) + 1
    tasks_db.append(task)
    return task

@router.get("/tasks/", response_model=List[Task])
def read_tasks():
    return tasks_db

@router.get("/tasks/{task_id}", response_model=Task)
def read_task(task_id: int):
    for task in tasks_db:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@router.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task: Task):
    for i, t in enumerate(tasks_db):
        if t.id == task_id:
            tasks_db[i] = task
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@router.delete("/tasks/{task_id}", response_model=Task)
def delete_task(task_id: int):
    for i, t in enumerate(tasks_db):
        if t.id == task_id:
            deleted_task = tasks_db.pop(i)
            return deleted_task
    raise HTTPException(status_code=404, detail="Task not found")

@router.post("/tasks/{task_id}/update_progress/")
def update_task_progress(task_id: int, progress: float):
    for i, t in enumerate(tasks_db):
        if t.id == task_id:
            if 0 <= progress <= 100:
                tasks_db[i].progress = progress
                return {"message": "Progress updated successfully"}
            else:
                raise HTTPException(status_code=422, detail="Invalid progress value")
    raise HTTPException(status_code=404, detail="Task not found")

@router.post("/tasks/{task_id}/assign/")
def assign_task(task_id: int, user_id: int):
    for i, t in enumerate(tasks_db):
        if t.id == task_id:
            tasks_db[i].assigned_to = user_id
            return {"message": "Task assigned successfully"}
    raise HTTPException(status_code=404, detail="Task not found")

@router.post("/tasks/{task_id}/notify/")
def notify_task(task_id: int):
    for i, t in enumerate(tasks_db):
        if t.id == task_id:
            # Implement notification logic here
            return {"message": "Notification sent successfully"}
    raise HTTPException(status_code=404, detail="Task not found")
