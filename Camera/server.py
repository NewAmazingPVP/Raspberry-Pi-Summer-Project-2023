#!/usr/bin/python3

import cv2
from flask import Flask, render_template, Response
from picamera2 import Picamera2
from libcamera import controls

app = Flask(__name__)
picam2 = None

def init_camera():
    global picam2
    cv2.startWindowThread()
    picam2 = Picamera2()
    picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (960, 540)}))
    picam2.start()
    picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous})
    picam2.set_controls({"AwbMode": controls.AwbModeEnum.Auto})
    picam2.set_controls({"AeConstraintMode": controls.AeConstraintModeEnum.Normal})
    picam2.set_controls({"AeExposureMode": controls.AeExposureModeEnum.Normal})
    picam2.set_controls({"AeMeteringMode": controls.AeMeteringModeEnum.Matrix})

def gen_frames():
    while True:
        frame = picam2.capture_array()
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue
        yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n\r\n'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    init_camera()
    app.run(host='0.0.0.0', port=5000, threaded=True)

