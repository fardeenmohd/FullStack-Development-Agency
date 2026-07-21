from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .database import get_db, Base, engine
from .routers import auth, dashboard, products, compute, transactions

app = FastAPI()

# Include routers
app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(products.router)
app.include_router(compute.router)
app.include_router(transactions.router)
