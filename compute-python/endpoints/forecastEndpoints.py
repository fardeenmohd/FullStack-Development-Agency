from flask import Blueprint, request, jsonify
from models import Forecast

forecast_bp = Blueprint('forecast', __name__)

@forecast_bp.route('/historical_data', methods=['GET'])
def get_historical_data():
    return _get_forecast_data(type='historical')

@forecast_bp.route('/market_trends', methods=['GET'])
def get_market_trends():
    return _get_forecast_data(type='trend')

@forecast_bp.route('/lead_conversion_rates', methods=['GET'])
def get_lead_conversion_rates():
    return _get_forecast_data(type='conversion_rate')

def _get_forecast_data(type):
    data = Forecast.query.filter_by(type=type).all()
    return jsonify([d.to_dict() for d in data])
