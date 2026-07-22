from flask import Flask, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Notification

app = Flask(__name__)

@app.route('/notifications', methods=['POST'])
@jwt_required()
def create_notification():
    current_user = get_jwt_identity()
    data = request.get_json()
    new_notification = Notification(user_id=current_user['id'], message=data['message'])
    new_notification.save()
    return jsonify({'message': 'Notification created successfully'}), 201

@app.route('/notifications', methods=['GET'])
@jwt_required()
def get_notifications():
    current_user = get_jwt_identity()
    notifications = Notification.query.filter_by(user_id=current_user['id']).all()
    return jsonify([{'id': n.id, 'message': n.message, 'read': n.read} for n in notifications])

@app.route('/notifications/<int:notification_id>', methods=['PUT'])
@jwt_required()
def update_notification(notification_id):
    current_user = get_jwt_identity()
    notification = Notification.query.filter_by(id=notification_id, user_id=current_user['id']).first_or_404()
    data = request.get_json()
    if 'read' in data:
        notification.read = data['read']
        notification.save()
    return jsonify({'message': 'Notification updated successfully'}), 200
