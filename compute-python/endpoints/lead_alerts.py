from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session
from database import get_db, Base, engine
from models import LeadAlert

app = FastAPI()

class LeadAlertCreate(BaseModel):
    name: str
    email_template_id: int
    trigger_condition: str

class LeadAlertUpdate(BaseModel):
    name: Optional[str] = None
    email_template_id: Optional[int] = None
    trigger_condition: Optional[str] = None

# Create the database tables
Base.metadata.create_all(bind=engine)

@app.post("/lead_alerts/", response_model=LeadAlert)
def create_lead_alert(lead_alert: LeadAlertCreate, db: Session = Depends(get_db)):
    new_lead_alert = LeadAlert(**lead_alert.dict())
    db.add(new_lead_alert)
    db.commit()
    db.refresh(new_lead_alert)
    return new_lead_alert

@app.get("/lead_alerts/", response_model=List[LeadAlert])
def read_lead_alerts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    lead_alerts = db.query(LeadAlert).offset(skip).limit(limit).all()
    return lead_alerts

@app.get("/lead_alerts/{lead_alert_id}", response_model=LeadAlert)
def read_lead_alert(lead_alert_id: int, db: Session = Depends(get_db)):
    lead_alert = get_lead_alert_by_id(lead_alert_id, db)
    if not lead_alert:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lead alert not found")
    return lead_alert

@app.put("/lead_alerts/{lead_alert_id}", response_model=LeadAlert)
def update_lead_alert(lead_alert_id: int, lead_alert_update: LeadAlertUpdate, db: Session = Depends(get_db)):
    lead_alert = get_lead_alert_by_id(lead_alert_id, db)
    if not lead_alert:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lead alert not found")
    update_data = lead_alert_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(lead_alert, key, value)
    db.commit()
    db.refresh(lead_alert)
    return lead_alert

@app.delete("/lead_alerts/{lead_alert_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_lead_alert(lead_alert_id: int, db: Session = Depends(get_db)):
    lead_alert = get_lead_alert_by_id(lead_alert_id, db)
    if not lead_alert:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lead alert not found")
    db.delete(lead_alert)
    db.commit()
    return {"detail": "Lead alert deleted"}

def get_lead_alert_by_id(lead_alert_id: int, db: Session) -> Optional[LeadAlert]:
    """Retrieve a lead alert by its ID."""
    return db.query(LeadAlert).filter(LeadAlert.id == lead_alert_id).first()
