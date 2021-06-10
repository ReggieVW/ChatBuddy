import os
import time
import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras import Model
from flask import Flask, request, Response, jsonify, send_file, make_response 
import cv2
import json
import numpy as np
from flask_cors import CORS
import base64
from datetime import datetime
#from camera import VideoCamera
import face_encoding.face_recognition_knn_training as faceRecog
from face_emotion.emotion_transformer import EmotionImage
import nlp.emofromtweet as EmotionNlp
from eliza.eliza import Eliza
import urllib
import io
from datetime import datetime
import glob
import csv
import os

# initialize the Haar Cascade face detection model
face_haar_cascade = cv2.CascadeClassifier(cv2.samples.findFile(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'))

app = Flask(__name__)
CORS(app)

@app.route('/register', methods=['POST'])
def register():
        print("register:")
    #try:   
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
        # Detect faces 
        gray= cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces_detected = face_haar_cascade.detectMultiScale(gray, 1.32, 5)
        if len(faces_detected) == 0:
            print("no face detected")
            return 'no face detected', 204
        # Added image for metric learning 
        directory_train = 'face_encoding/images-train'
        if not os.path.exists(directory_train):
            os.makedirs(directory_train)
        faceRecog.add_image(directory_train, image, username)
        faceRecog.train(directory_train, "face_encoding/trained_knn_model.clf")
        os.remove(path)   
        return json.dumps({"register": str("OK")})
    #except:
     #   return 'error', 500

def check_user_exist(imagePath):
    # Check if user exist based on feature vectors 
    predictions = faceRecog.predict_face(imagePath, "face_encoding/trained_knn_model.clf")
    if(predictions):
        name = predictions[0][0]
    else:
        name = "unknown"
    return name

@app.route('/verify', methods=['POST'])
def verification():
    print("verify:")
    img_data = request.get_json()['image64']
    img_name = str(int(datetime.timestamp(datetime.now())))
    directory = './images'
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(directory+'/'+img_name+'.jpg', "wb") as fh:
        fh.write(base64.b64decode(img_data[22:]))
    path = directory+'/'+img_name+'.jpg'
    image = cv2.imread(path)
    name = check_user_exist(path)
    os.remove(path)
    if name == "unknown":
        print("unknown face")
        return 'unknown face', 204
    return json.dumps({"identity": str(name)})
    
@app.route('/uploadEmotionImage', methods=['POST'])
def upload_emotion_image():
    print("upload_emotion_image:")
    img_name = ""
    img_data = request.get_json()['image64']
    profilename = request.get_json()['profilename']
    img_name = str(int(datetime.timestamp(datetime.now())))
    directory = './images/'+str(profilename)+'/'
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(directory+'/'+img_name+'.jpg', "wb") as fh:
        fh.write(base64.b64decode(img_data[22:]))
    # write temp image file
    temp_image_path = directory+'/'+img_name+'.jpg'
    img = cv2.imread(temp_image_path)
    # Get predictions using CNN
    transformed_img, label = EmotionImage.transform(img)
    # write results to CSV file
    try:
        csv_directory = './result'
        if not os.path.exists(csv_directory):
            os.makedirs(csv_directory)
        path_csv = os.path.join(csv_directory, 'emotions.csv')
        with open(path_csv, 'a+', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([datetime.now(),'CNN',label])
    except Exception as e:
        print("Error writing csv file "+e)
    # write image file with predictions
    path_transformed = directory+'/'+img_name+'_pred.jpg'
    cv2.imwrite(path_transformed, transformed_img)
    print("written file "+ path_transformed)
    os.remove(temp_image_path)
    return json.dumps({"uploaded": str("OK")})

@app.route('/getEmotionImages')
def get_emotion_image():
    print("getEmotionImage:")
    profile_name = request.args.get('profilename')
    directory = './images/'+str(profile_name)+'/'
    # Get latest prediction file
    list_of_files = glob.glob(directory+'/*pred.jpg') 
    latest_file = max(list_of_files, key=os.path.getctime)
    print("Get file =", latest_file)
    file = open(latest_file, 'rb')
    byte_io = io.BytesIO()
    byte_io.write(file.read())
    byte_io.seek(0)
    response = make_response(send_file(byte_io,mimetype='image/jpg'))
    response.headers['Content-Transfer-Encoding']='base64'
    return response 
    
@app.route('/chatEliza')
def chat_eliza():
    print("chatEliza:")
    eliza = Eliza()
    message = request.args.get('chatMessage')
    if(message):
        output = eliza.respond(message)
    else:
        output = "How are you feeling today?"
    print("message: "+output)
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    data = {"response": str(output), "time":dt_string}
    return json.dumps(data)
    
@app.route('/analyzeSentimentText')
def analyze_emotion_text():
    print("emotionDetectionText:")
    if request.args.get('text') is None:
        return json.dumps({"error": "Mandatory parameter missing"})
    sent = request.args.get('text')
    label, pred = EmotionNlp.predict(sent)
    return json.dumps({"label": str(label) + " ("+str(pred) + ")"})
    
@app.route('/time')
def time():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    return json.dumps({"time": str(current_time)})
    
#@app.route('/video_feed')
#def video_feed():
#    print("video_feed")
#    cam = VideoCamera()
#    return Response(gen(cam),
#                    mimetype='multipart/x-mixed-replace; boundary=frame')
                                              
                    
#def gen(camera):
#    while True:
#        frame = camera.get_frame()
#        yield (b'--frame\r\n'
#               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

if __name__ == "__main__":
    app.run(debug=False, threaded=True)