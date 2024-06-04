#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import logging
import time
from PIL import Image, ImageDraw, ImageFont
from waveshare_epd import epd2in13bc  # For tri-color display
# from waveshare_epd import epd2in13bc  # Update to the correct module for tri-color display

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Paths for fonts and images
imgdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'images')
fontdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts')

# Function to update the display with the first design
def update_display_design1(product_name, price):
    try:
        # Create blank images for black and red content
        Himage = Image.new('1', (epd.height, epd.width), 255)  # 255: white
        Rimage = Image.new('1', (epd.height, epd.width), 255)  # For red ink

        draw_black = ImageDraw.Draw(Himage)
        draw_red = ImageDraw.Draw(Rimage)

        logging.info("Drawing the price tag...")
        draw_black.rectangle((0, 0, epd.height, epd.width), fill=255)  # Clear background (white)
        draw_red.rectangle((0, 0, epd.height, epd.width), fill=255)  # Clear background (white)

        # Draw the OXXO logo in black
        logo_path = os.path.join(imgdir, 'oxxo.png')
        if os.path.exists(logo_path):
            logo = Image.open(logo_path)
            logo = logo.resize((80, 40))  # Resize logo to fit the display
            Himage.paste(logo, (10, 10))

        # Draw product name in black
        draw_black.text((100, 10), product_name, font=font24, fill=0)  # 0: black

        # Draw price in red
        draw_red.text((100, 60), price, font=font24, fill=0)  # 0: red

        # Display the image on the e-paper display
        epd.display(epd.getbuffer(Himage), epd.getbuffer(Rimage))
        logging.info("Updated display with new content")

    except IOError as e:
        logging.error(e)

# Function to update the display with the second design
def update_display_design2(product_name, price, volume, discount, barcode_text):
    try:
        # Create blank images for black and red content
        Himage = Image.new('1', (epd.height, epd.width), 255)  # 255: white
        Rimage = Image.new('1', (epd.height, epd.width), 255)  # For red ink

        draw_black = ImageDraw.Draw(Himage)
        draw_red = ImageDraw.Draw(Rimage)

        logging.info("Drawing the price tag...")
        draw_black.rectangle((0, 0, epd.height, epd.width), fill=255)  # Clear background (white)
        draw_red.rectangle((0, 0, 90, epd.width), fill=0)  # Red background for the left section

        # Draw red content
        draw_red.text((10, 10), "NOW", font=font24, fill=255)  # White text on red background
        draw_red.text((10, 40), price, font=font24, fill=255)
        draw_red.text((10, 70), f"SAVE\n{discount}%", font=font18, fill=255)

        # Draw product image and name in black
        product_image_path = os.path.join(imgdir, 'takis.png')
        if os.path.exists(product_image_path):
            product_image = Image.open(product_image_path)
            product_image = product_image.resize((80, 40))  # Resize image to fit the display
            Himage.paste(product_image, (100, 10))
        
        draw_black.text((100, 60), product_name, font=font24, fill=0)  # Black text for product name
        draw_black.text((100, 90), volume, font=font18, fill=0)
        draw_black.rectangle((100, 120, 220, 130), fill=0)  # Placeholder for barcode
        draw_black.text((100, 140), barcode_text, font=font18, fill=0)

        # Display the image on the e-paper display
        epd.display(epd.getbuffer(Himage), epd.getbuffer(Rimage))
        logging.info("Updated display with new content")

    except IOError as e:
        logging.error(e)

# Function to update the display with the third design
def update_display_design3(product_name, volume, price_per_liter, price, barcode_text):
    try:
        # Create a blank image for black content
        Himage = Image.new('1', (epd.height, epd.width), 255)  # 255: white

        draw_black = ImageDraw.Draw(Himage)

        logging.info("Drawing the price tag...")
        draw_black.rectangle((0, 0, epd.height, epd.width), fill=255)  # Clear background (white)

        # Draw product name and volume
        draw_black.text((10, 10), f"{product_name} x {volume}", font=font24, fill=0)  # 0: black

        # Draw price per liter
        draw_black.text((10, 40), f"Precio por litro\n${price_per_liter}", font=font18, fill=0)

        # Draw main price
        draw_black.text((10, 80), f"${price}", font=font24, fill=0)

        # Draw barcode
        draw_black.rectangle((10, 130, 180, 150), fill=0)  # Placeholder for barcode
        draw_black.text((10, 160), barcode_text, font=font18, fill=0)

        # Display the image on the e-paper display
        epd.display(epd.getbuffer(Himage))
        logging.info("Updated display with new content")

    except IOError as e:
        logging.error(e)


# Initialize the e-paper display
epd = epd2in13bc.EPD()
logging.info("init and Clear")
epd.init()
epd.Clear()

# Load fonts
font24 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttf'), 24)
font18 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttf'), 18)  # Smaller font size

# Main loop
try:
    while True:
         # Choose the design to display
        design_choice = 3  # Change to 1 to display the first design, 2 for the second design

        if design_choice == 1:
            update_display_design1('Takis', '$20.99')
        elif design_choice == 2:
            update_display_design2('Takis', '$15.99', '280g', '50', '123456789012')
        elif design_choice == 3:
            update_display_design3('Coca Cola', '2.25L', '15.00', '33.75', '7702004003508')
        
        # Wait for some time before updating again
        time.sleep(10)  # Update every 10 seconds

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd2in13d.epdconfig.module_exit(cleanup=True)
    exit()
