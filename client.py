import requests
import time

def fetch_data():
    """Fetch data from the Raspberry Pi 4 server."""
    try:
        response = requests.get('http://<Pi4-IP-Address>:5000/get_data')
        if response.status_code == 200:
            return response.json()
        else:
            print("Failed to fetch data: ", response.status_code)
    except requests.exceptions.RequestException as e:
        print("HTTP Request failed: ", e)
    return None

def update_display(data):
    """Simulate updating the ESL display with the fetched data."""
    # This would be replaced with actual code to update the ESL hardware.
    print("Display updated with: ", data)

def main_loop():
    while True:
        data = fetch_data()
        if data:
            update_display(data)
        time.sleep(60)  # Poll every minute

if __name__ == "__main__":
    main_loop()
