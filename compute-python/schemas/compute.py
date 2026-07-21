from pydantic import BaseModel, Field, field_validator
from uuid import UUID
from typing import List, Optional

class HuntLeadsRequest(BaseModel):
    exporter_id: UUID
    product_name: str = Field(..., min_length=1, max_length=255)
    hs_code: str = Field(..., min_length=2, max_length=12)
    description: str
    target_regions: List[str] = Field(..., min_items=1)

    @field_validator("target_regions")
    @classmethod
    def validate_regions(cls, v: List[str]) -> List[str]:
        valid_regions = {"OM", "CN", "EU", "AU"}
        normalized = []
        for region in v:
            reg_upper = region.upper()
            if reg_upper not in valid_regions:
                # Fallback check for full names or other formats
                pass
            normalized.append(reg_upper)
        return normalized

class LeadResponseItem(BaseModel):
    id: UUID
    exporter_id: UUID
    company_name: str
    country: str
    contact_email: Optional[str] = None
    confidence_score: float = Field(..., ge=0.0, le=100.0)
    source_url: Optional[str] = None
    status: str = "NEW"

class HuntLeadsResponse(BaseModel):
    status: str = "success"
    leads_found: int
    data: List[LeadResponseItem]

class ScoreLeadRequest(BaseModel):
    lead_id: UUID
    company_name: str
    country: str
    hs_code: str = Field(..., min_length=2, max_length=12)
    source_url: Optional[str] = None

class RiskAssessment(BaseModel):
    legitimacy_rating: str  # HIGH, MEDIUM, LOW
    compliance_risk: str    # HIGH, MEDIUM, LOW
    sanction_check: str     # PASSED, FAILED
    nlp_alignment_score: float = Field(..., ge=0.0, le=1.0)

class ScoreLeadResponse(BaseModel):
    lead_id: UUID
    confidence_score: float = Field(..., ge=0.0, le=100.0)
    risk_assessment: RiskAssessment
    analysis_summary: str
