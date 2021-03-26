# Import all the necessary files!
import os
import time
import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras import Model
from flask import Flask, request, Response, jsonify
import cv2
import json
import numpy as np
from flask_cors import CORS
import base64
from datetime import datetime
from camera import VideoCamera
from face_encoding.encoding_scan_pickle import FaceEncodingPickle

# initialize the Haar Cascade face detection model
face_haar_cascade = cv2.CascadeClassifier(cv2.samples.findFile(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'))

app = Flask(__name__)
CORS(app)

@app.route('/register', methods=['POST'])
def register():
    try:
        username = request.get_json()['username']
        img_data = request.get_json()['image64']
        img_name = str(int(datetime.timestamp(datetime.now())))
        directory = 'images'
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(directory+'/'+img_name+'.jpg', "wb") as fh:
            fh.write(base64.b64decode(img_data[22:]))
        path = directory + '/'+img_name+'.jpg'
        image = cv2.imread(path)
        gray= cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces_detected = face_haar_cascade.detectMultiScale(gray, 1.32, 5)
        if len(faces_detected) == 0:
            print("no face detected")
            data = {"register": 0, "status":204}
            return json.dumps(data)
        if not os.path.exists("known_faces"):
            os.makedirs("known_faces")
        faceRecog = FaceEncodingPickle("known_faces")
        faceRecog.add_image(image, username)
        os.remove(path)   
        return json.dumps({"register": str("OK")})
    except:
        return json.dumps({"status": 500})

def check_user_exist(image):
    faceRecog = FaceEncodingPickle("known_faces")
    name = faceRecog.scan_image(image)
    return name

@app.route('/verify', methods=['POST'])
def verification():
    print("verify:")
    img_data = request.get_json()['image64']
    img_name = str(int(datetime.timestamp(datetime.now())))
    directory = 'images'
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(directory+'/'+img_name+'.jpg', "wb") as fh:
        fh.write(base64.b64decode(img_data[22:]))
    path = 'images/'+img_name+'.jpg'
    image = cv2.imread(path)
    name = check_user_exist(image)
    os.remove(path)
    if name == "unknown":
        return json.dumps({"identity": 0})
    return json.dumps({"identity": str(name)})
    
@app.route('/video_feed')
def video_feed():
    print("video_feed testing")
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
                    
@app.route('/test')
def test():
    print("name testing")
    data = {'name': 'reginald'}
    return jsonify(data)
    
@app.route('/time')
def get_current_time():
    return {'time': time.time()}
                    
def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

if __name__ == "__main__":
    app.run(debug=True)