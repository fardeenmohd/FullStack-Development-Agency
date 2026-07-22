from flask import Flask, request, jsonify
from services.conversionRateService import ConversionRateService

app = Flask(__name__)
conversion_rate_service = ConversionRateService()

@app.route('/api/conversion-rate', methods=['GET'])
def get_conversion_rate():
    date_range = request.args.get('dateRange')
    if not date_range:
        return jsonify({'error': 'Date range is required'}), 400
    rate = conversion_rate_service.get_conversion_rate(date_range)
    return jsonify(rate)

@app.route('/api/conversion-rate', methods=['POST'])
def create_conversion_rate():
    data = request.json
    if not data or 'date' not in data or 'rate' not in data:
        return jsonify({'error': 'Invalid data'}), 400
    conversion_rate_service.create_conversion_rate(data['date'], data['rate'])
    return jsonify({'message': 'Conversion rate created successfully'}), 201

@app.route('/api/conversion-rate/<int:id>', methods=['PUT'])
def update_conversion_rate(id):
    data = request.json
    if not data or 'rate' not in data:
        return jsonify({'error': 'Invalid data'}), 400
    conversion_rate_service.update_conversion_rate(id, data['rate'])
    return jsonify({'message': 'Conversion rate updated successfully'}), 200

@app.route('/api/conversion-rate/<int:id>', methods=['DELETE'])
def delete_conversion_rate(id):
    conversion_rate_service.delete_conversion_rate(id)
    return jsonify({'message': 'Conversion rate deleted successfully'}), 204
