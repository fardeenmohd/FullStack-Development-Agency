from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your-secret-key'
jwt = JWTManager(app)

# Dummy data for tasks and users
tasks = {}
users = {}

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if username != 'admin' or password != 'password':
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

@app.route('/tasks', methods=['POST'])
@jwt_required()
def assign_task():
    current_user = get_jwt_identity()
    task_id = request.json.get('task_id')
    user_id = request.json.get('user_id')

    if not current_user or not task_id or not user_id:
        return jsonify({"msg": "Missing data"}), 400

    if user_id not in users:
        return jsonify({"msg": "User not found"}), 404

    tasks[task_id] = {'user': user_id, 'status': 'assigned'}
    return jsonify({"msg": "Task assigned successfully"})

@app.route('/tasks/<task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    current_user = get_jwt_identity()
    new_status = request.json.get('status')

    if not current_user or not task_id or not new_status:
        return jsonify({"msg": "Missing data"}), 400

    if task_id not in tasks:
        return jsonify({"msg": "Task not found"}), 404

    if tasks[task_id]['user'] != current_user and current_user != 'admin':
        return jsonify({"msg": "Unauthorized"}), 403

    tasks[task_id]['status'] = new_status
    return jsonify({"msg": "Task updated successfully"})

@app.route('/tasks/<task_id>/notify', methods=['POST'])
@jwt_required()
def notify_task(task_id):
    current_user = get_jwt_identity()

    if not current_user or not task_id:
        return jsonify({"msg": "Missing data"}), 400

    if task_id not in tasks:
        return jsonify({"msg": "Task not found"}), 404

    if tasks[task_id]['user'] != current_user and current_user != 'admin':
        return jsonify({"msg": "Unauthorized"}), 403

    # Logic to send notification
    return jsonify({"msg": "Notification sent successfully"})

if __name__ == '__main__':
    app.run(debug=True)
