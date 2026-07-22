from flask import Flask, request, jsonify
from services.forecastService import ForecastService

app = Flask(__name__)
forecast_service = ForecastService()

@app.route('/api/v1/forecast/predict', methods=['POST'])
def predict_forecast():
    data = request.get_json()
    predictions = forecast_service.predict_conversion_rates(data)
    return jsonify(predictions)

if __name__ == '__main__':
    app.run(debug=True)
