from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

router = APIRouter()

class LeadAlert(BaseModel):
    id: int
    user_id: int
    target_regions: List[str]
    product_categories: List[str]
    confidence_score_threshold: float

# In-memory storage for alerts (replace with database in production)
alerts_db = []

def find_alert(alert_id: int) -> Optional[LeadAlert]:
    """Helper function to find an alert by ID."""
    return next((alert for alert in alerts_db if alert.id == alert_id), None)

@router.post("/alerts/", response_model=LeadAlert)
def create_lead_alert(alert: LeadAlert):
    alerts_db.append(alert)
    return alert

@router.get("/alerts/", response_model=List[LeadAlert])
def get_all_lead_alerts():
    return alerts_db

@router.get("/alerts/{alert_id}", response_model=LeadAlert)
def get_lead_alert(alert_id: int):
    alert = find_alert(alert_id)
    if alert:
        return alert
    raise HTTPException(status_code=404, detail="Alert not found")

@router.put("/alerts/{alert_id}", response_model=LeadAlert)
def update_lead_alert(alert_id: int, updated_alert: LeadAlert):
    alert = find_alert(alert_id)
    if alert:
        alerts_db[alerts_db.index(alert)] = updated_alert
        return updated_alert
    raise HTTPException(status_code=404, detail="Alert not found")

@router.delete("/alerts/{alert_id}", response_model=LeadAlert)
def delete_lead_alert(alert_id: int):
    alert = find_alert(alert_id)
    if alert:
        alerts_db.remove(alert)
        return alert
    raise HTTPException(status_code=404, detail="Alert not found")
