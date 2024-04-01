from flask import Flask, render_template, Response
import os
import math
import time
import numpy as np
import pygame
import busio
import board
from scipy.interpolate import griddata
from colour import Color
import adafruit_amg88xx
from PIL import Image
from io import BytesIO

app = Flask(__name__)

@app.route('/thermal_plot')
def thermal_plot():
    while True:
        i2c_bus = busio.I2C(board.SCL, board.SDA)
        sensor = adafruit_amg88xx.AMG88XX(i2c_bus)

        MINTEMP = 10.0
        MAXTEMP = 22.0
        COLORDEPTH = 1024

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

