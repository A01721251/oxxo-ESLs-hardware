#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import time  # Import the time module
import logging
from PIL import Image, ImageDraw, ImageFont, ImageOps
from waveshare_epd import epd2in13b_V4  # Change to epd2in13b_V4

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Paths for fonts and images
imgdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'images')
fontdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts')

# Function to convert images to a compatible format
def convert_image(image_path, size):
    try:
        image = Image.open(image_path)
        if image.mode == 'P':  # Handle palette-based images with transparency
            image = image.convert("RGBA")
        image = image.convert("L")  # Convert to grayscale
        image = ImageOps.invert(image)  # Invert colors
        image = image.resize(size, Image.LANCZOS)
        image = image.convert("1")  # Convert to binary (black and white)
        return image
    except IOError as e:
        logging.error(f"Error converting image: {e}")
        return None

# Function to update the display with the desired design
def update_display_design(product_name, volume, original_price, discount_price):
    try:
        epd = epd2in13b_V4.EPD()  # Initialize the display for the new model
        logging.info("init and Clear")
        epd.init()
        epd.Clear()
        time.sleep(1)

        # Create blank images for black and red content
        black_image = Image.new('1', (epd.height, epd.width), 255)  # 255: white
        red_image = Image.new('1', (epd.height, epd.width), 255)  # For red ink

        draw_black = ImageDraw.Draw(black_image)
        draw_red = ImageDraw.Draw(red_image)

        logging.info("Drawing the price tag...")
        draw_black.rectangle((0, 0, epd.height, epd.width), fill=255)  # Clear background (white)

        # Load fonts
        font12 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttf'), 12)
        font14 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttf'), 14)
        font16 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttf'), 16)
        font20 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttf'), 22)

        # Load and draw the OXXO logo
        logo_path = os.path.join(imgdir, 'oxxo.png')
        if os.path.exists(logo_path):
            logo = convert_image(logo_path, (60, 25))
            if logo:
                black_image.paste(logo, (10, 10))

        # Draw product name and volume
        draw_black.text((10, 40), f"{product_name}", font=font14, fill=0)
        draw_black.text((10, 60), f"{volume}", font=font12, fill=0)

        # Load and draw the barcode
        barcode_path = os.path.join(imgdir, 'barcode2.png')
        if os.path.exists(barcode_path):
            barcode = convert_image(barcode_path, (70, 20))
            if barcode:
                black_image.paste(barcode, (10, 80))

        # Calculate half height and center the rectangle vertically
        half_height = (epd.width - 40)
        y_start = (epd.width - half_height) // 2

        # Draw the red price tag area
        draw_red.rectangle((epd.height // 2, y_start, epd.height - 5, y_start + half_height), fill=0)  # Red background

        # Measure the width of the text to ensure the line strikes through the entire text
        text_width, text_height = draw_red.textsize(f"${original_price}", font=font14)

        # Draw the original price text
        draw_red.text((epd.height // 2 + 5, y_start), f"${original_price}", font=font14, fill=255)

        # Define extra width and height for the strike-through line
        extra_width = 12  # Adjust this value as needed
        extra_height = 3  # Adjust this value as needed

        # Draw the thicker strike-through line
        draw_red.line(
            (
                epd.height // 2 + 5 - extra_width // 2,               # Start X (left side)
                y_start + text_height // 2 - extra_height // 2,       # Start Y (slightly above center)
                epd.height // 2 + 5 + text_width + extra_width // 2,  # End X (right side)
                y_start + text_height // 2 + extra_height // 2        # End Y (slightly below center)
            ), 
            fill=255, width=extra_height
        )

        # Draw the discount price below the original price
        draw_red.text((epd.height // 2 + 5, y_start + text_height + 10), f"${discount_price}", font=font20, fill=255)  # Discount price

        # Rotate images for horizontal display
        black_image = black_image.rotate(90, expand=True)
        red_image = red_image.rotate(90, expand=True)

        # Save images for debugging
        black_image.save(os.path.join(imgdir, 'black_image_debug.png'))
        red_image.save(os.path.join(imgdir, 'red_image_debug.png'))

        # Display the image on the e-paper display
        epd.display(epd.getbuffer(black_image), epd.getbuffer(red_image))
        logging.info("Updated display with new content")

    except IOError as e:
        logging.error(e)

# Initialize the e-paper display
epd = epd2in13b_V4.EPD()
logging.info("init and Clear")
epd.init()
epd.Clear()

# Update the display with a sample design
update_display_design('Coca Cola', '355 ml', '12.20', '10.00')

# Don't clear or put the display to sleep, just exit the script
logging.info("Display update complete, exiting script.")
