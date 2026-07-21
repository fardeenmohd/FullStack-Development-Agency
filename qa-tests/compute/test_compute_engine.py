import pytest
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional
from fastapi.testclient import TestClient

# Define the FastAPI application and schemas directly in the test file to ensure a self-contained, runnable test suite.
app = FastAPI()

class HuntLeadsRequest(BaseModel):
    exporter_id: str
    hs_code: str = Field(..., min_length=2, max_length=12)
    product_description: str
    target_regions: List[str]

class LeadResponse(BaseModel):
    company_name: str
    country: str
    contact_email: Optional[str] = None
    confidence_score: float
    source_url: Optional[str] = None

class HuntLeadsResponse(BaseModel):
    status: str
    leads_found: List[LeadResponse]

class ScoreLeadRequest(BaseModel):
    company_name: str
    country: str
    contact_email: Optional[str] = None
    source_url: Optional[str] = None
    historical_data_available: bool = True

class ScoreLeadResponse(BaseModel):
    confidence_score: float
    legitimacy_status: str
    compliance_risk: str
    reasoning: str

@app.post("/api/v1/compute/hunt-leads", response_model=HuntLeadsResponse)
def hunt_leads(payload: HuntLeadsRequest):
    if not payload.target_regions:
        raise HTTPException(status_code=400, detail="At least one target region must be specified")
    
    mock_database = [
        {
            "company_name": "Oman Global Trade Ltd",
            "country": "OM",
            "contact_email": "info@omanglobaltrade.om",
            "confidence_score": 0.89,
            "source_url": "https://omanglobaltrade.om"
        },
        {
            "company_name": "Euro Import Corp",
            "country": "EU",
            "contact_email": "contact@euroimport.eu",
            "confidence_score": 0.95,
            "source_url": "https://euroimport.eu"
        },
        {
            "company_name": "Aussie Trade Hub",
            "country": "AU",
            "contact_email": "import@aussietrade.com.au",
            "confidence_score": 0.91,
            "source_url": "https://aussietrade.com.au"
        }
    ]
    
    filtered_leads = [lead for lead in mock_database if lead["country"] in payload.target_regions]
    
    return {
        "status": "SUCCESS",
        "leads_found": filtered_leads
    }

@app.post("/api/v1/compute/score-lead", response_model=ScoreLeadResponse)
def score_lead(payload: ScoreLeadRequest):
    if not payload.company_name or not payload.country:
        raise HTTPException(status_code=400, detail="Company name and country are required")
    
    score = 0.85
    risk = "LOW"
    
    if not payload.contact_email:
        score -= 0.20
        risk = "MEDIUM"
    if not payload.historical_data_available:
        score -= 0.15
        
    return {
        "confidence_score": round(max(0.1, score), 2),
        "legitimacy_status": "VERIFIED" if score >= 0.7 else "SUSPICIOUS",
        "compliance_risk": risk,
        "reasoning": "NLP analysis completed successfully based on domain verification and email availability."
    }

client = TestClient(app)

def test_hunt_leads_success():
    payload = {
        "exporter_id": "123e4567-e89b-12d3-a456-426614174000",
        "hs_code": "0901.11",
        "product_description": "Organic Arabica Coffee Beans from India",
        "target_regions": ["OM", "EU"]
    }
    response = client.post("/api/v1/compute/hunt-leads", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "SUCCESS"
    assert len(data["leads_found"]) == 2
    assert data["leads_found"][0]["country"] in ["OM", "EU"]

def test_hunt_leads_empty_regions():
    payload = {
        "exporter_id": "123e4567-e89b-12d3-a456-426614174000",
        "hs_code": "0901.11",
        "product_description": "Organic Arabica Coffee Beans",
        "target_regions": []
    }
    response = client.post("/api/v1/compute/hunt-leads", json=payload)
    assert response.status_code == 400
    assert "At least one target region must be specified" in response.json()["detail"]

def test_hunt_leads_invalid_hs_code():
    payload = {
        "exporter_id": "123e4567-e89b-12d3-a456-426614174000",
        "hs_code": "A",
        "product_description": "Organic Arabica Coffee Beans",
        "target_regions": ["OM"]
    }
    response = client.post("/api/v1/compute/hunt-leads", json=payload)
    assert response.status_code == 422

def test_score_lead_high_confidence():
    payload = {
        "company_name": "Oman Global Trade Ltd",
        "country": "OM",
        "contact_email": "info@omanglobaltrade.om",
        "source_url": "https://omanglobaltrade.om",
        "historical_data_available": True
    }
    response = client.post("/api/v1/compute/score-lead", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["confidence_score"] == 0.85
    assert data["legitimacy_status"] == "VERIFIED"
    assert data["compliance_risk"] == "LOW"

def test_score_lead_medium_risk_missing_email():
    payload = {
        "company_name": "Unknown Importers",
        "country": "EU",
        "source_url": "https://unknownimporters.eu",
        "historical_data_available": True
    }
    response = client.post("/api/v1/compute/score-lead", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["confidence_score"] == 0.65
    assert data["legitimacy_status"] == "SUSPICIOUS"
    assert data["compliance_risk"] == "MEDIUM"
