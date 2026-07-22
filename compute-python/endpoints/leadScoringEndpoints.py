from flask import Flask, jsonify, request

app = Flask(__name__)

# Dummy data for demonstration purposes
leads_data = [
    {"id": 1, "score": 85, "conversion_rate": 0.2, "compliance_risk": 0.1},
    {"id": 2, "score": 75, "conversion_rate": 0.15, "compliance_risk": 0.2}
]

def get_lead_by_id(lead_id):
    """Retrieve a lead by its ID."""
    return next((lead for lead in leads_data if lead['id'] == lead_id), None)

@app.route('/api/lead-scoring', methods=['GET'])
def get_lead_scores():
    """Return all lead scores."""
    return jsonify(leads_data)

@app.route('/api/lead-scoring/<int:lead_id>', methods=['GET'])
def get_lead_score(lead_id):
    """Retrieve a specific lead score by ID."""
    lead = get_lead_by_id(lead_id)
    if lead:
        return jsonify(lead)
    else:
        return jsonify({"error": "Lead not found"}), 404

@app.route('/api/lead-scoring/conversion-rate', methods=['GET'])
def get_conversion_rate():
    """Calculate and return the overall conversion rate."""
    total_leads = len(leads_data)
    converted_leads = sum(1 for lead in leads_data if lead['conversion_rate'] > 0)
    conversion_rate = (converted_leads / total_leads) * 100 if total_leads > 0 else 0
    return jsonify({"conversion_rate": conversion_rate})

@app.route('/api/lead-scoring/compliance-risk', methods=['GET'])
def get_compliance_risk():
    """Calculate and return the overall compliance risk."""
    total_leads = len(leads_data)
    high_risk_leads = sum(1 for lead in leads_data if lead['compliance_risk'] > 0.1)
    compliance_risk = (high_risk_leads / total_leads) * 100 if total_leads > 0 else 0
    return jsonify({"compliance_risk": compliance_risk})

if __name__ == '__main__':
    app.run(debug=True)
