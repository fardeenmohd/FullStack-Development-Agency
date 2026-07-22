from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
import os

app = Flask(__name__)
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
if not JWT_SECRET_KEY:
    raise EnvironmentError("JWT_SECRET_KEY environment variable must be set")
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
jwt = JWTManager(app)

# Dummy data for product listings and tasks
products = [
    {'id': 1, 'name': 'Product A', 'status': 'pending'},
    {'id': 2, 'name': 'Product B', 'status': 'in_progress'}
]
tasks = []

def find_item_by_id(items, item_id):
    """Helper function to find an item by its ID."""
    return next((item for item in items if item['id'] == item_id), None)

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if username != 'admin' or password != 'password':
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

@app.route('/products', methods=['GET'])
@jwt_required()
def get_products():
    current_user = get_jwt_identity()
    if current_user != 'admin':
        return jsonify({"msg": "Access denied"}), 403
    return jsonify(products)

@app.route('/products/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    current_user = get_jwt_identity()
    if current_user != 'admin':
        return jsonify({"msg": "Access denied"}), 403

    product = find_item_by_id(products, product_id)
    if not product:
        return jsonify({"msg": "Product not found"}), 404

    data = request.get_json()
    product.update(data)
    return jsonify(product)

@app.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    current_user = get_jwt_identity()
    if current_user != 'admin':
        return jsonify({"msg": "Access denied"}), 403

    data = request.get_json()
    task_id = max([t['id'] for t in tasks] or [0]) + 1
    task = {'id': task_id, **data}
    tasks.append(task)
    return jsonify(task)

@app.route('/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    current_user = get_jwt_identity()
    if current_user != 'admin':
        return jsonify({"msg": "Access denied"}), 403

    task = find_item_by_id(tasks, task_id)
    if not task:
        return jsonify({"msg": "Task not found"}), 404

    data = request.get_json()
    task.update(data)
    return jsonify(task)

@app.route('/tasks/<int:task_id>/progress', methods=['PUT'])
@jwt_required()
def update_task_progress(task_id):
    current_user = get_jwt_identity()
    if current_user != 'admin':
        return jsonify({"msg": "Access denied"}), 403

    task = find_item_by_id(tasks, task_id)
    if not task:
        return jsonify({"msg": "Task not found"}), 404

    data = request.get_json()
    if 'progress' in data and isinstance(data['progress'], int) and 0 <= data['progress'] <= 100:
        task['progress'] = data['progress']
        return jsonify(task)
    else:
        return jsonify({"msg": "Invalid progress value"}), 400

@app.route('/products/<int:product_id>/assign_task', methods=['POST'])
@jwt_required()
def assign_task_to_product(product_id):
    current_user = get_jwt_identity()
    if current_user != 'admin':
        return jsonify({"msg": "Access denied"}), 403

    product = find_item_by_id(products, product_id)
    if not product:
        return jsonify({"msg": "Product not found"}), 404

    task_data = request.get_json()
    task_id = max([t['id'] for t in tasks] or [0]) + 1
    task = {'id': task_id, **task_data}
    tasks.append(task)
    product['assigned_task'] = task_id
    return jsonify(product)

@app.route('/products/<int:product_id>/unassign_task', methods=['POST'])
@jwt_required()
def unassign_task_from_product(product_id):
    current_user = get_jwt_identity()
    if current_user != 'admin':
        return jsonify({"msg": "Access denied"}), 403

    product = find_item_by_id(products, product_id)
    if not product:
        return jsonify({"msg": "Product not found"}), 404

    if 'assigned_task' in product:
        task_id = product.pop('assigned_task')
        tasks = [t for t in tasks if t['id'] != task_id]
    return jsonify(product)

@app.route('/products/<int:product_id>/real_time_update', methods=['PUT'])
@jwt_required()
def real_time_update_product(product_id):
    current_user = get_jwt_identity()
    if current_user != 'admin':
        return jsonify({"msg": "Access denied"}), 403

    product = find_item_by_id(products, product_id)
    if not product:
        return jsonify({"msg": "Product not found"}), 404

    data = request.get_json()
    product.update(data)
    return jsonify(product)

if __name__ == '__main__':
    app.run(debug=True)
