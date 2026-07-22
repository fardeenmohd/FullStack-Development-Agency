from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///alerts.db'
db = SQLAlchemy(app)

class Alert(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(db.String(36), nullable=False)
    criteria = db.Column(db.JSON, nullable=False)

@app.route('/api/v1/alerts', methods=['POST'])
def create_alert():
    data = request.get_json()
    if not validate_payload(data):
        return jsonify({'error': 'Invalid payload'}), 400

    alert = Alert(
        id=str(uuid.uuid4()),
        user_id=data['user_id'],
        criteria=data['criteria']
    )
    db.session.add(alert)
    db.session.commit()

    # Trigger background job to check for matching leads
    from .jobs import check_leads_for_alerts
    check_leads_for_alerts.delay([alert.id])

    return jsonify({'message': 'Alert created successfully'}), 201

def validate_payload(data):
    """Validate the incoming payload."""
    return data and 'user_id' in data and 'criteria' in data

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
