# Python FastAPI Compute Engine Services Test Suite

import pytest
from services import lead_hunter_service, score_lead_service

# Mock data for testing
mock_user_id = '123e4567-e89b-12d3-a456-426614174000'
mock_product_data = {
    "exporter_id": mock_user_id,
    "name": "Electronics",
    "hs_code": "0301.90.00",
    "description": "High-quality electronics for export",
    "target_regions": ["OM", "CN"]
}
mock_lead_data = {
    "exporter_id": mock_user_id,
    "company_name": "ABC Corp",
    "country": "OM",
    "confidence_score": 0.95
}

# Test the lead hunting service
@pytest.mark.parametrize('hs_code, target_regions', [
    ('0301.90.00', ['OM']),
    ('0702.90.00', ['CN'])
])
def test_hunt_leads_service(hs_code, target_regions):
    leads = lead_hunter_service.hunt_leads(hs_code, target_regions)
    assert isinstance(leads, list)

# Test the lead scoring service
@pytest.mark.parametrize('confidence_score', [
    0.95,
    0.85
])
def test_score_lead_service(confidence_score):
    score = score_lead_service.score_lead(confidence_score)
    assert isinstance(score, float)
