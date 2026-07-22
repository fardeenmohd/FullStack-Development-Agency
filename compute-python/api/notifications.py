from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notifications.db'
app.config['JWT_SECRET_KEY'] = 'your-secret-key'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_type = db.Column(db.String(80), nullable=False)
    notification_preference = db.Column(db.String(20), nullable=False)
    target_recipients = db.Column(db.String(120), nullable=False)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(username=data['username'], password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and bcrypt.check_password_hash(user.password_hash, data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify({'access_token': access_token}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/notifications', methods=['POST'])
@jwt_required()
def create_notification():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    new_notification = Notification(
        user_id=current_user_id,
        event_type=data['event_type'],
        notification_preference=data['notification_preference'],
        target_recipients=data['target_recipients']
    )
    db.session.add(new_notification)
    db.session.commit()
    return jsonify({'message': 'Notification created successfully'}), 201

@app.route('/notifications', methods=['GET'])
@jwt_required()
def get_notifications():
    current_user_id = get_jwt_identity()
    notifications = Notification.query.filter_by(user_id=current_user_id).all()
    notification_list = [{'id': n.id, 'event_type': n.event_type, 'notification_preference': n.notification_preference, 'target_recipients': n.target_recipients} for n in notifications]
    return jsonify(notification_list), 200

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
