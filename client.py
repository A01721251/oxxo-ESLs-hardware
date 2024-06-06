import requests
import time
from waveshare_epd import epd2in13_V2
from display import update_display_design2
from flask import Flask, request, jsonify

app = Flask(__name__)

esl_id = str(49)

@app.route('/update_display', methods=['POST'])
def update_display():
    data = request.json
    print(f"Received data: {data}")
    changes = data.get('changes', {})
    if changes:
        etiqueta_id, price_info = list(changes.items())[0]  # Get the first item
        
        if etiqueta_id != esl_id:
            return jsonify({"status": "This is not a CocaCola product. Skipping..."}), 200
                
        new_price = price_info.get('new_price')
        update_display_design2('Takis', f"${str(new_price)}", '280g', '50', '123456789012')
        return jsonify({"status": "Display updated"}), 200
    else:
        return jsonify({"status": "No changes to display"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)