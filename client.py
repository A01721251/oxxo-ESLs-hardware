import requests
import time
from waveshare_epd import epd2in13_V2
from PIL import Image, ImageDraw, ImageFont

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
    """Update the Waveshare e-Paper display with the fetched data."""
    try:
        epd = epd2in13_V2.EPD()
        epd.init(epd.FULL_UPDATE)
        epd.Clear(0xFF)  # Clear the display to white

        # Load an image
        image = Image.open('path/to/your/logo.bmp')
        bmp = image.resize((epd.height, epd.width), Image.ANTIALIAS)
        
        # Create a new image with white background
        display_image = Image.new('1', (epd.height, epd.width), 255)
        draw = ImageDraw.Draw(display_image)
        
        # Position the image at the top center of the display
        display_image.paste(bmp, (0,0))
        
        # Add text below the image
        font = ImageFont.load_default()
        draw.text((10, 100), 'Price: {}'.format(data['price']), font = font, fill = 0)
        
        # Display the image and text
        epd.display(epd.getbuffer(display_image))
        epd.sleep()

    except IOError as e:
        print(e)

def main_loop():
    while True:
        data = fetch_data()
        if data:
            update_display(data)
        time.sleep(60)  # Poll every minute

if __name__ == "__main__":
    main_loop()
