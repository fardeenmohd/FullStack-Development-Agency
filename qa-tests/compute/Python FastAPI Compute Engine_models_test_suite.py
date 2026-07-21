# Python FastAPI Compute Engine Models Test Suite

import pytest
from models import Lead, Product

# Mock data for testing
mock_lead_data = {
    "exporter_id": '123e4567-e89b-12d3-a456-426614174000',
    "company_name": "ABC Corp",
    "country": "OM",
    "confidence_score": 0.95
}
mock_product_data = {
    "exporter_id": '123e4567-e89b-12d3-a456-426614174000',
    "name": "Electronics",
    "hs_code": "0301.90.00",
    "description": "High-quality electronics for export",
    "target_regions": ["OM", "CN"]
}

# Test the Lead model
@pytest.mark.parametrize('data', [
    mock_lead_data,
])
def test_lead_model(data):
    lead = Lead(**data)
    assert lead.exporter_id == data['exporter_id']
    assert lead.company_name == data['company_name']
    assert lead.country == data['country']
    assert lead.confidence_score == data['confidence_score']

# Test the Product model
@pytest.mark.parametrize('data', [
    mock_product_data,
])
def test_product_model(data):
    product = Product(**data)
    assert product.exporter_id == data['exporter_id']
    assert product.name == data['name']
    assert product.hs_code == data['hs_code']
    assert product.description == data['description']
    assert product.target_regions == data['target_regions']
