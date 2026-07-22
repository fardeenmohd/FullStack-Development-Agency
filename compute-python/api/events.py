from flask import Flask, request, jsonify
import requests
import logging
from celery import Celery

app = Flask(__name__)

# Mock notification service URL
NOTIFICATION_SERVICE_URL = "http://notification-service:5000/send"

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('event_api')

# Initialize Celery
celery_app = Celery(app.name, broker='redis://localhost:6379/0')
celery_app.conf.update(app.config)

@celery_app.task
def send_notification_task(user_id, message, notification_type):
    payload = {
        'user_id': user_id,
        'message': message,
        'notification_type': notification_type
    }
    
    try:
        response = requests.post(NOTIFICATION_SERVICE_URL, json=payload)
        if response.status_code != 200:
            logger.error(f"Failed to send notification: {response.text}")
        else:
            logger.info(f"Notification sent successfully for user {user_id}: {message}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Request exception occurred: {e}")

@app.route('/trigger_event', methods=['POST'])
def trigger_event():
    data = request.json
    event_type = data.get('event_type')
    user_id = data.get('user_id')
    preferences = data.get('preferences')

    if not event_type or not user_id or not preferences:
        return jsonify({"error": "Missing required fields"}), 400

    # Logic to handle different types of events
    notification_message = f"{event_type.capitalize()} detected for you!"
    notification_type = preferences.get('notification_type', 'email')

    if event_type in ['new_lead', 'transaction_status_change', 'product_catalog_update']:
        send_notification_task.delay(user_id, notification_message, notification_type)
    else:
        return jsonify({"error": "Unsupported event type"}), 400

    return jsonify({"message": "Event triggered and notification sent successfully"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
