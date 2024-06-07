#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import logging
from PIL import Image, ImageDraw, ImageFont, ImageOps
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
        
        # Draw the left side background in black
        draw_black.rectangle((0, 0, epd.height // 2, epd.width), fill=0)  # Black background on the left side

        # Draw product name in white on the black background
        draw_black.text((10, 10), product_name, font=font24, fill=255)  # 255: white

        # Draw price in white on the black background
        draw_black.text((10, 50), price, font=font24, fill=255)  # 255: white

        # Load the OXXO logo and prepare it for drawing
        logo_path = os.path.join(imgdir, 'oxxo.png')
        if os.path.exists(logo_path):
            logo = Image.open(logo_path).convert("RGBA")
            logo_w, logo_h = logo.size
            max_size = (epd.height , epd.width)  # Scaling down to half the display size
            logo.thumbnail(max_size, Image.ANTIALIAS)

            # Position the logo on the right side, centered vertically in the right half
            logo_x = epd.height // 2 + (epd.height // 2 - logo.size[0]) // 2
            logo_y = (epd.width - logo.size[1]) // 2

            # Create an image with the red parts of the logo
            # red_logo = Image.new("1", logo.size, 255)
            # for y in range(logo.size[1]):
            #     for x in range(logo.size[0]):
            #         r, g, b, a = logo.getpixel((x, y))
            #         if r > 200 and g < 50 and b < 50 and a > 0:  # Red parts
            #             red_logo.putpixel((x, y), 0)

            # Paste the red parts onto the red image
            Rimage.paste(logo, (logo_x, logo_y))

        # Draw product name in black
        # draw_black.text((10, 10), product_name, font=font24, fill=0)  # 0: black

        # # Draw price in red
        # draw_red.text((10, 50), price, font=font24, fill=0)  # 0: red

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
        
# Function to convert images to a compatible format
def convert_image(image_path, size):
    image = Image.open(image_path)
    if image.mode == 'P':  # Handle palette-based images with transparency
        image = image.convert("RGBA")
    image = image.convert("L")  # Convert to grayscale
    image = ImageOps.invert(image)  # Invert colors
    image = image.resize(size, Image.LANCZOS)
    image = image.convert("1")  # Convert to binary (black and white)
    return image

# Function to update the display with the desired design
def update_display_design(product_name, volume, original_price, discount_price, barcode_text):
    try:
        # Create blank images for black and red content
        Himage = Image.new('1', (epd.height, epd.width), 255)  # 255: white
        Rimage = Image.new('1', (epd.height, epd.width), 255)  # For red ink

        draw_black = ImageDraw.Draw(Himage)
        draw_red = ImageDraw.Draw(Rimage)

        logging.info("Drawing the price tag...")
        draw_black.rectangle((0, 0, epd.height, epd.width), fill=255)  # Clear background (white)

        # Load fonts
        font12 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttf'), 12)
        font14 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttf'), 14)
        font16 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttf'), 16)
        font20 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttf'), 20)

        # Load and draw the OXXO logo
        logo_path = os.path.join(imgdir, 'oxxo.png')
        if os.path.exists(logo_path):
            logo = convert_image(logo_path, (60, 25))
            Himage.paste(logo, (10, 10))

        # Draw product name and volume
        draw_black.text((10, 40), f"{product_name}", font=font14, fill=0)
        draw_black.text((10, 60), f"{volume}", font=font12, fill=0)

        # Load and draw the barcode
        barcode_path = os.path.join(imgdir, 'barcode2.png')
        if os.path.exists(barcode_path):
            barcode = convert_image(barcode_path, (120, 50))
            Himage.paste(barcode, (10, 70))

        # Calculate half height and center the rectangle vertically
        half_height = (epd.width - 40)
        y_start = (epd.width - half_height) // 2

        # Draw the red price tag area
        draw_red.rectangle((epd.height // 2, y_start, epd.height - 5, y_start + half_height), fill=0)  # Red background
        
        # Measure the width of the text to ensure the line strikes through the entire text
        text_width, text_height = draw_red.textsize(f"${original_price}", font=font12)

        # Draw the original price text
        draw_red.text((epd.height // 2 + 5, y_start), f"${original_price}", font=font12, fill=255)

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
        Himage = Himage.rotate(90, expand=True)
        Rimage = Rimage.rotate(90, expand=True)

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
# font24 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttf'), 18)  # Replace 'YourFont.ttf' with the actual font file name
# font18 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttf'), 14)  # Smaller font size

# Choose the design to display
design_choice = 4  # Change to 1 for the first design, 2 for the second design, 3 for the third design

if design_choice == 1:
    update_display_design1('Takis', '$2.99')
elif design_choice == 2:
    update_display_design2('Takis', '$0.99', '280g', '50', '123456789012')
elif design_choice == 3:
    update_display_design3('Coca Cola', '2.25L', '15.00', '33.75', '7702004003508')
elif design_choice == 4:
    # Update the display with the desired design
    update_display_design('Coca Cola', '355 ml', '12.20', '11.00', '0 35545 62336 78 1')

# Don't clear or put the display to sleep, just exit the script
logging.info("Display update complete, exiting script.")
