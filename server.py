from flask import Flask, jsonify
import requests
from apscheduler.schedulers.background import BackgroundScheduler


app = Flask(__name__)

# Store the latest data fetched from the backend
latest_data = {}

ap_id = 1

def fetch_data_from_backend():
    """Simulate fetching data from the remote backend."""
    response = requests.get(f'https://oxxo-esls-backend.onrender.com/api/hardware/AP/{ap_id}')
    if response.status_code == 200:
        return response.json()
    return {}

def compare_prices(old_data, new_data):
    """
    Compare old data with new data and return changes.
    Both old_data and new_data should be lists of dictionaries.
    """
    updated_prices = {}
    # Create a quick lookup for old prices
    old_prices = {item['etiqueta_id']: item for item in old_data}

    for item in new_data:
        etiqueta_id = item['etiqueta_id']
        old_item = old_prices.get(etiqueta_id)
        if old_item and old_item['precio_actual'] != item['precio_actual']:
            updated_prices[etiqueta_id] = {
                'old_price': old_item['precio_actual'],
                'new_price': item['precio_actual']
            }
    return updated_prices

def push_data_to_esl(data):
    """Push the latest data to the ESL device."""
    try:
        response = requests.post(f'http://{esl_ip}:5001/update_display', json=data)
        print(f"Pushed data to ESL: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to push data to ESL: {e}")

@app.route('/update_data')
def update_data():
    """Endpoint to trigger a manual update of the data from the backend."""
    global latest_data
    new_data = fetch_data_from_backend()
    price_changes = compare_prices(latest_data, new_data)
    latest_data = new_data  # Update the latest_data with the new fetch
    if price_changes:
        push_data_to_esl({"status": "Data updated", "changes": price_changes})
    return jsonify({"status": "Data updated", "changes": price_changes})


@app.route('/get_data')
def get_data():
    """Endpoint for Pi Zeros to fetch the latest pricing data."""
    return jsonify(latest_data)

def scheduled_task():
    try:
        response = requests.get('http://localhost:5050/update_data')
        print(f"Scheduled task response: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Error reaching endpoint: {e}")

if __name__ == '__main__':
    latest_data = fetch_data_from_backend()  # Initial fetch

    # Setup APScheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(scheduled_task, 'interval', seconds=5)
    scheduler.start()

    # Run Flask app
    app.run(host='0.0.0.0', port=5050)