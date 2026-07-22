from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/lead_pipeline', methods=['GET'])
def get_lead_pipeline():
    # Example data for demonstration purposes
    lead_pipeline_data = {
        "timeline": [
            {"step": "Lead Scoring", "status": "Completed", "score": 85},
            {"step": "Notification Triggers", "status": "Pending"},
            {"step": "Transaction Initiation", "status": "Not Started"}
        ]
    }
    
    return jsonify(lead_pipeline_data)

if __name__ == '__main__':
    app.run(debug=True)
