from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
import os
import secrets

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notifications.db'
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', secrets.token_urlsafe(32))  # Use environment variable or generate a secure secret key
db = SQLAlchemy(app)
jwt = JWTManager(app)

class UserSubscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    event_type = db.Column(db.String(50), nullable=False)
    notification_method = db.Column(db.String(20), nullable=False)  # email, SMS
    target_recipients = db.Column(db.String(255), nullable=True)

def validate_subscription_data(data):
    required_fields = ['event_type', 'notification_method']
    if not all(key in data for key in required_fields):
        return False, {'message': 'Missing required fields'}, 400

    event_types = ['new_lead', 'transaction_status_change', 'product_catalog_update']
    notification_methods = ['email', 'SMS']

    if data['event_type'] not in event_types:
        return False, {'message': 'Invalid event type'}, 400

    if data['notification_method'] not in notification_methods:
        return False, {'message': 'Invalid notification method'}, 400

    return True, None, 200

@app.route('/subscribe', methods=['POST'])
@jwt_required()
def subscribe():
    current_user = get_jwt_identity()
    data = request.get_json()

    is_valid, error_message, status_code = validate_subscription_data(data)
    if not is_valid:
        return jsonify(error_message), status_code

    new_subscription = UserSubscription(
        user_id=current_user['id'],
        event_type=data['event_type'],
        notification_method=data['notification_method'],
        target_recipients=data.get('target_recipients', '')
    )
    db.session.add(new_subscription)
    db.session.commit()

    return jsonify({'message': 'Subscription successful'}), 201

@app.route('/subscriptions', methods=['GET'])
@jwt_required()
def get_subscriptions():
    current_user = get_jwt_identity()
    subscriptions = UserSubscription.query.filter_by(user_id=current_user['id']).all()
    subscription_list = [{'event_type': sub.event_type, 'notification_method': sub.notification_method, 'target_recipients': sub.target_recipients} for sub in subscriptions]
    return jsonify(subscription_list), 200

if __name__ == '__main__':
    app.run(debug=True)
