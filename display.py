#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import logging
from PIL import Image, ImageDraw, ImageFont
from waveshare_epd import epd2in13bc  # For tri-color display

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

        # Load the OXXO logo and prepare it for drawing
        logo_path = os.path.join(imgdir, 'oxxo.png')
        if os.path.exists(logo_path):
            logo = Image.open(logo_path)
            logo = logo.convert("RGBA")
            logo_w, logo_h = logo.size
            max_size = (epd.height - 20, epd.width - 20)  # Leaving some margin
            logo.thumbnail(max_size, Image.ANTIALIAS)

            # Center the logo on the display
            logo_x = (epd.height - logo.size[0]) // 2
            logo_y = (epd.width - logo.size[1]) // 2

            # Split the logo into its red and black parts
            red_channel = logo.getchannel('R')
            black_white_image = ImageOps.invert(red_channel).convert('1')  # Inverted red for black/white display

            # Draw the logo parts
            Rimage.paste(logo, (logo_x, logo_y), mask=red_channel)
            Himage.paste(black_white_image, (logo_x, logo_y), mask=black_white_image)

        # Draw product name in black
        draw_black.text((10, 10), product_name, font=font24, fill=0)  # 0: black

        # Draw price in red
        draw_red.text((10, 50), price, font=font24, fill=0)  # 0: red

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
        # Create blank images for black and red content
        Himage = Image.new('1', (epd.height, epd.width), 255)  # 255: white
        Rimage = Image.new('1', (epd.height, epd.width), 255)  # For red ink

        draw_black = ImageDraw.Draw(Himage)
        draw_red = ImageDraw.Draw(Rimage)

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
        epd.display(epd.getbuffer(Himage), epd.getbuffer(Rimage))
        logging.info("Updated display with new content")

    except IOError as e:
        logging.error(e)

# Initialize the e-paper display
epd = epd2in13bc.EPD()
logging.info("init and Clear")
epd.init()
epd.Clear()

# Load fonts
font24 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttf'), 24)  # Replace 'YourFont.ttf' with the actual font file name
font18 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttf'), 18)  # Smaller font size

# Choose the design to display
design_choice = 1  # Change to 1 for the first design, 2 for the second design, 3 for the third design

if design_choice == 1:
    update_display_design1('Takis', '$2.99')
elif design_choice == 2:
    update_display_design2('Takis', '$0.99', '280g', '50', '123456789012')
elif design_choice == 3:
    update_display_design3('Coca Cola', '2.25L', '15.00', '33.75', '7702004003508')

# Don't clear or put the display to sleep, just exit the script
logging.info("Display update complete, exiting script.")
