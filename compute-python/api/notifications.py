from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notifications.db'
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Change this!
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
    current_user_id = get_jwt_identity()
    is_valid, error_response, status_code = validate_subscription_data(request.get_json())

    if not is_valid:
        return jsonify(error_response), status_code

    subscription = UserSubscription.query.filter_by(user_id=current_user_id, event_type=request.json['event_type']).first()
    
    if subscription:
        subscription.notification_method = request.json['notification_method']
        subscription.target_recipients = request.json.get('target_recipients', None)
    else:
        new_subscription = UserSubscription(
            user_id=current_user_id,
            event_type=request.json['event_type'],
            notification_method=request.json['notification_method'],
            target_recipients=request.json.get('target_recipients', None)
        )
        db.session.add(new_subscription)
    
    try:
        db.session.commit()
        return jsonify({'message': 'Subscription updated successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to update subscription', 'error': str(e)}), 500

@app.route('/notifications', methods=['POST'])
@jwt_required()
def create_notification():
    current_user_id = get_jwt_identity()
    is_valid, error_response, status_code = validate_subscription_data(request.get_json())

    if not is_valid:
        return jsonify(error_response), status_code

    event_types = ['new_lead', 'transaction_status_change', 'product_catalog_update']

    subscriptions = UserSubscription.query.filter_by(event_type=request.json['event_type']).all()

    for subscription in subscriptions:
        if subscription.notification_method == 'email':
            send_email(subscription.target_recipients, request.json['message'])
        elif subscription.notification_method == 'SMS':
            send_sms(subscription.target_recipients, request.json['message'])

    return jsonify({'message': 'Notification sent successfully'}), 201

def send_email(recipients, message):
    # Implement email sending logic here
    pass

def send_sms(recipients, message):
    # Implement SMS sending logic here
    pass

@app.route('/automated_notifications', methods=['POST'])
@jwt_required()
def create_automated_notification():
    current_user_id = get_jwt_identity()
    is_valid, error_response, status_code = validate_subscription_data(request.get_json())

    if not is_valid:
        return jsonify(error_response), status_code

    subscription = UserSubscription.query.filter_by(user_id=current_user_id, event_type=request.json['event_type']).first()
    
    if subscription:
        subscription.notification_method = request.json['notification_method']
        subscription.target_recipients = request.json.get('target_recipients', None)
    else:
        new_subscription = UserSubscription(
            user_id=current_user_id,
            event_type=request.json['event_type'],
            notification_method=request.json['notification_method'],
            target_recipients=request.json.get('target_recipients', None)
        )
        db.session.add(new_subscription)
    
    try:
        db.session.commit()
        return jsonify({'message': 'Automated notification created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to create automated notification', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
