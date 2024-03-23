from flask import Flask, Response
from picamera2 import Picamera2, Preview
import time

app = Flask(__name__)

# Initialize the camera
camera = Picamera2()

# Configure preview
preview_config = camera.create_preview_configuration(main={"size": (800, 600)})
camera.configure(preview_config)

# Start the preview
#camera.start_preview(Preview.QTGL)

# Start the camera
camera.start()

@app.route('/')
def index():
    return render_template('index.html')  # You need to create index.html for your frontend

def generate_frames():
    while True:
        # Capture a JPEG image and return its data
        metadata = camera.capture_file("test.jpg")
        with open("test.jpg", "rb") as f:
            frame = f.read()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

