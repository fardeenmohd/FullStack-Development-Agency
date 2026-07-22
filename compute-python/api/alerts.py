from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///alerts.db'
db = SQLAlchemy(app)

class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(80), nullable=False)
    alert_name = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(120), nullable=False)
    region = db.Column(db.String(120), nullable=False)

def validate_data(data, required_fields):
    if not data or any(field not in data for field in required_fields):
        return False
    return True

@app.route('/alerts', methods=['POST'])
def create_alert():
    data = request.get_json()
    if not validate_data(data, ['user_id', 'alert_name', 'category', 'region']):
        return jsonify({'error': 'Invalid input'}), 400
    new_alert = Alert(**data)
    db.session.add(new_alert)
    db.session.commit()
    return jsonify({'message': 'Alert created successfully'}), 201

@app.route('/alerts/<int:id>', methods=['PUT'])
def update_alert(id):
    data = request.get_json()
    if not validate_data(data, ['user_id', 'alert_name', 'category', 'region']):
        return jsonify({'error': 'Invalid input'}), 400
    alert = Alert.query.get(id)
    if not alert:
        return jsonify({'error': 'Alert not found'}), 404
    for key, value in data.items():
        setattr(alert, key, value)
    db.session.commit()
    return jsonify({'message': 'Alert updated successfully'}), 200

@app.route('/alerts/<int:id>', methods=['DELETE'])
def delete_alert(id):
    alert = Alert.query.get(id)
    if not alert:
        return jsonify({'error': 'Alert not found'}), 404
    db.session.delete(alert)
    db.session.commit()
    return jsonify({'message': 'Alert deleted successfully'}), 200

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
