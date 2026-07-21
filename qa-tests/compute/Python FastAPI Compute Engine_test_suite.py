# Python FastAPI Compute Engine Test Suite

import pytest
from fastapi.testclient import TestClient
from main import app, lead_hunter_engine, score_lead_engine

# Initialize the test client
client = TestClient(app)

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

# Test the lead hunting endpoint
@pytest.mark.parametrize('hs_code, target_regions', [
    ('0301.90.00', ['OM']),
    ('0702.90.00', ['CN'])
])
def test_hunt_leads(hs_code, target_regions):
    response = client.post(
        '/api/v1/compute/hunt-leads',
        json={'hs_code': hs_code, 'target_regions': target_regions}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Test the lead scoring endpoint
@pytest.mark.parametrize('confidence_score', [
    0.95,
    0.85
])
def test_score_lead(confidence_score):
    response = client.post(
        '/api/v1/compute/score-lead',
        json={'confidence_score': confidence_score}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert 'score' in response.json()
