from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)

    product = relationship("Product", back_populates="tasks")
    user = relationship("User", back_populates="assigned_tasks")
