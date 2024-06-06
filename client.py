import requests
import time
from waveshare_epd import epd2in13_V2
from display import update_display_design2

def fetch_data():
    """Fetch data from the Raspberry Pi 4 server."""
    try:
        response = requests.get('http://localhost:5050/get_data')
        if response.status_code == 200:
            return response.json()
        else:
            print("Failed to fetch data: ", response.status_code)
    except requests.exceptions.RequestException as e:
        print("HTTP Request failed: ", e)
    return None

def update_display(data):
    """Update the Waveshare e-Paper display with the fetched data."""
    try:
        product_price = data.get('product_price')
        update_display_design2('Takis', product_price, '280g', '50', '123456789012')
        print("Updated display with new content")
    except IOError as e:
        print(e)

def main_loop():
    while True:
        data = fetch_data()
        if data:
            update_display(data)
        time.sleep(5)  # Poll every minute

if __name__ == "__main__":
    main_loop()
