#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import logging
import time
from PIL import Image, ImageDraw, ImageFont
from waveshare_epd import epd2in13d

# Set up logging
logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("epd2in13d Demo")

    # Initialize and clear the display
    epd = epd2in13d.EPD()
    logging.info("init and Clear")
    epd.init()
    epd.Clear()

    # Create a blank image for drawing
    Himage = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(Himage)

    # Drawing the price tag
    logging.info("Drawing the price tag...")
    draw.rectangle((0, 0, epd.height, epd.width), fill=255)  # Clear background

    # Draw product name
    draw.text((10, 10), 'Takis', fill=0)

    # Draw price
    draw.text((10, 50), '$2.99', fill=0)

    # Display the image on the e-paper display
    epd.display(epd.getbuffer(Himage))
    time.sleep(2)

    logging.info("Clear...")
    epd.init()
    epd.Clear()

    logging.info("Goto Sleep...")
    epd.sleep()

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd2in13d.epdconfig.module_exit(cleanup=True)
    exit()
