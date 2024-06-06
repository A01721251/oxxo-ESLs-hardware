import requests
import time
from waveshare_epd import epd2in13_V2
from display import update_display_design2
from flask import Flask, request, jsonify

app = Flask(__name__)

# def fetch_data():
#     """Fetch data from the Raspberry Pi 4 server."""
#     try:
#         response = requests.get('http://192.168.99.218:5050/update_data')
#         if response.status_code == 200:
#             return response.json()
#         else:
#             print("Failed to fetch data: ", response.status_code)
#     except requests.exceptions.RequestException as e:
#         print("HTTP Request failed: ", e)
#     return None

# def update_display(data):
#     """Update the Waveshare e-Paper display with the fetched data."""
#     try:
#         print("Received data:", data)  # Print the received data to understand its format
#         if isinstance(data, list):
#             print("Unexpected data format")
#             return
        
#         if isinstance(data, dict):
#             changes = data.get('changes', {})
#             if changes:
#                 # Assuming you want the first change in the dictionary
#                 etiqueta_id, price_info = list(changes.items())[0]  # Get the first item
                
#                 if etiqueta_id != '49':
#                     print("This is not a CocaCola product. Skipping...")
#                     return
                
#                 new_price = price_info.get('new_price')

#                 # Call update_display_design2 with the new price
#                 update_display_design2('Takis', f"${str(new_price)}", '280g', '50', '123456789012')
#                 print("Updated display with new content")
#             else:
#                 print("No price changes available to display")
#         else:
#             print("Unexpected data format")
#     except IOError as e:
#         print(e)

@app.route('/update_display', methods=['POST'])
def update_display():
    data = request.json
    print(f"Received data: {data}")
    changes = data.get('changes', {})
    if changes:
        etiqueta_id, price_info = list(changes.items())[0]  # Get the first item
        
        if etiqueta_id != '49':
            return jsonify({"status": "This is not a CocaCola product. Skipping..."}), 200
                
        new_price = price_info.get('new_price')
        update_display_design2('Takis', f"${str(new_price)}", '280g', '50', '123456789012')
        return jsonify({"status": "Display updated"}), 200
    else:
        return jsonify({"status": "No changes to display"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)