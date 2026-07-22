from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/transactions', methods=['POST'])
def create_transactions():
    data = request.get_json()
    lead_ids = data.get('lead_ids')

    if not lead_ids:
        return jsonify({'error': 'No lead IDs provided'}), 400

    # Logic to handle transaction creation based on lead IDs
    # For example, save the transactions to a database or perform other operations

    return jsonify({'message': f'Transactions created for {len(lead_ids)} leads.'}), 201

if __name__ == '__main__':
    app.run(debug=True)
