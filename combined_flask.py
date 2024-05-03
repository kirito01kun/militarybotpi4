from picamera2 import Picamera2, Preview
import time
from flask import Flask, render_template, Response
import os
import math
import numpy as np
import pygame
import busio
import board
import libcamera
from scipy.interpolate import griddata
from colour import Color
import adafruit_amg88xx
from PIL import Image, ImageOps
from io import BytesIO
import stable
import cv2

app = Flask(__name__)

# Initialize the camera
camera = Picamera2()

# Configure preview
preview_config = camera.create_preview_configuration(main={"size": (800, 600)})

#preview_config["transform"] = libcamera.Transform(hflip=1, vflip=0)
camera.configure(preview_config)

# Start the preview
#camera.start_preview(Preview.QTGL)

# Start the camera
camera.start()

MAX_TEMP = None


def generate_frames():
    while True:
        # Capture a JPEG image and return its data
        metadata = camera.capture_file("test.jpg")
        
        # Read the captured image using OpenCV
        frame = cv2.imread("test.jpg")

        # Flip the image vertically if MPU is not detected
        if stable.STABLE < 0:
            frame = cv2.flip(frame, 0)  # Flip along the vertical axis

        # Encode the flipped image to JPEG format
        _, jpeg_frame = cv2.imencode('.jpg', frame)

        # Yield the JPEG frame
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg_frame.tobytes() + b'\r\n')

   
@app.route('/thermal_plot')
def thermal_plot():
    global MAX_TEMP
    while True:
        i2c_bus = busio.I2C(board.SCL, board.SDA)
        sensor = adafruit_amg88xx.AMG88XX(i2c_bus)

        MINTEMP = 10.0
        MAXTEMP = 21.0
        COLORDEPTH = 1024
        
        temp = max(max(row) for row in sensor.pixels)
        MAX_TEMP = temp if int(temp) != 0 else MAX_TEMP

        points = [(math.floor(ix / 8), (ix % 8)) for ix in range(0, 64)]
        grid_x, grid_y = np.mgrid[0:7:32j, 0:7:32j]

        height = 480
        width = 480

        blue = Color("indigo")
        colors = list(blue.range_to(Color("red"), COLORDEPTH))
        colors = [(int(c.red * 255), int(c.green * 255), int(c.blue * 255)) for c in colors]

        displayPixelWidth = width / 30
        displayPixelHeight = height / 30

        lcd = pygame.Surface((width, height))

        pixels = []
        for row in sensor.pixels:
            pixels = pixels + row
        pixels = [map_value(p, MINTEMP, MAXTEMP, 0, COLORDEPTH - 1) for p in pixels]

        bicubic = griddata(points, pixels, (grid_x, grid_y), method="cubic")

        for ix, row in enumerate(bicubic):
            for jx, pixel in enumerate(row):
                pygame.draw.rect(
                    lcd,
                    colors[constrain(int(pixel), 0, COLORDEPTH - 1)],
                    (
                        displayPixelHeight * ix,
                        displayPixelWidth * jx,
                        displayPixelHeight,
                        displayPixelWidth,
                    ),
                )

        img_str = pygame.image.tostring(lcd, 'RGB')
        image = Image.frombytes('RGB', (width, height), img_str)
        if(stable.STABLE > 0):
            image = image.rotate(270)
        else:
            image = image.rotate(90)
        #image = image.transpose(Image.FLIP_LEFT_RIGHT)
        img_io = BytesIO()
        image.save(img_io, format='JPEG')
        img_io.seek(0)

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + img_io.getvalue() + b'\r\n')

        time.sleep(0.1)  # Adjust the sleep time as needed

def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))

def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

@app.route('/th')
def thermal_feed():
    return Response(thermal_plot(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/vd')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
 

