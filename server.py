from flask import Flask, jsonify
import requests

app = Flask(__name__)

# Store the latest data fetched from the backend
latest_data = {}

def fetch_data_from_backend():
    """Simulate fetching data from the remote backend."""
    response = requests.get('https://yourbackend.example.com/api/prices')
    if response.status_code == 200:
        return response.json()
    return {}

@app.route('/update_data')
def update_data():
    """Endpoint to trigger a manual update of the data from the backend."""
    global latest_data
    latest_data = fetch_data_from_backend()
    return jsonify({"status": "Data updated", "data": latest_data})

@app.route('/get_data')
def get_data():
    """Endpoint for Pi Zeros to fetch the latest pricing data."""
    return jsonify(latest_data)

if __name__ == '__main__':
    latest_data = fetch_data_from_backend()  # Initial fetch
    app.run(host='0.0.0.0', port=5000)
