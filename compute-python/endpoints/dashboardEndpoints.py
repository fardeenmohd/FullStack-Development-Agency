from flask import Blueprint, jsonify

dashboard_bp = Blueprint('dashboard', __name__)

def fetch_data(endpoint):
    if endpoint == '/api/trade-metrics':
        data = {
            'total_trades': 1234,
            'average_trade_value': 5678.90,
            'highest_trade_value': 9876.54
        }
    elif endpoint == '/api/active-leads':
        data = [
            {'id': 1, 'name': 'Lead A'},
            {'id': 2, 'name': 'Lead B'}
        ]
    elif endpoint == '/api/transaction-statuses':
        data = {
            'pending': 3,
            'completed': 15,
            'failed': 2
        }
    else:
        return None

    return jsonify(data)

@dashboard_bp.route('/api/trade-metrics', methods=['GET'])
def get_trade_metrics():
    return fetch_data('/api/trade-metrics')

@dashboard_bp.route('/api/active-leads', methods=['GET'])
def get_active_leads():
    return fetch_data('/api/active-leads')

@dashboard_bp.route('/api/transaction-statuses', methods=['GET'])
def get_transaction_statuses():
    return fetch_data('/api/transaction-statuses')
