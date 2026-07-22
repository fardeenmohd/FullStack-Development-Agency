from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

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

    # Assuming the existence of a User model for SQLAlchemy ORM
    created_by: "User" = relationship("User", foreign_keys=[created_by_id])
    updated_by: Optional["User"] = relationship("User", foreign_keys=[updated_by_id])

# Assuming the existence of a database model for SQLAlchemy ORM
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    created_by_id = Column(Integer, ForeignKey("users.id"), index=True)
    updated_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    comments = relationship("Comment", back_populates="product")
    task_assignments = relationship("TaskAssignment", back_populates="product")
    progress = relationship("Progress", uselist=False, back_populates="product")

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    product_id = Column(Integer, ForeignKey("products.id"), index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    product = relationship("Product", back_populates="comments")

class TaskAssignment(Base):
    __tablename__ = "task_assignments"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    product_id = Column(Integer, ForeignKey("products.id"), index=True)
    status = Column(String, index=True)
    assigned_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    product = relationship("Product", back_populates="task_assignments")

class Progress(Base):
    __tablename__ = "progress"
    id = Column(Integer, primary_key=True, index=True)
    percentage_complete = Column(Float, index=True)
    last_updated = Column(DateTime, default=datetime.utcnow)
    product_id = Column(Integer, ForeignKey("products.id"), index=True)

    product = relationship("Product", back_populates="progress")
