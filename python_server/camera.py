import cv2
import numpy as np
from keras.models import model_from_json
from keras.preprocessing import image
from keras.models import load_model
from keras.preprocessing.image import img_to_array

# initialize the Haar Cascade face detection model
face_haar_cascade = cv2.CascadeClassifier(cv2.samples.findFile(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'))
#load weights
model =load_model(r'\facial_sentiment\Emotion_face.h5')

class_labels = ['Angry', 'Happy', 'Neutral', 'Sad', 'Surprise']

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    # returns camera frames along with bounding boxes and predictions
    def get_frame(self):
        ret,img= self.video.read()# captures frame and returns boolean value and captured image
        gray= cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces_detected = face_haar_cascade.detectMultiScale(gray, 1.32, 5)
        if len(faces_detected) != 0:
            for (x, y, w, h) in faces_detected:
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),thickness=7)
                roi_gray = gray[y:y+h,x:x+w]
                roi_gray = cv2.resize(roi_gray,(48,48),interpolation=cv2.INTER_AREA)

                if np.sum([roi_gray])!=0:
                    roi = roi_gray.astype('float')/255.0
                    roi = img_to_array(roi)
                    roi = np.expand_dims(roi,axis=0)

                    # make a prediction on the ROI, then lookup the class
                    preds = model.predict(roi)[0]
                    label=class_labels[preds.argmax()]
                    label_position = (x,y)
                    cv2.putText(img,label,label_position,cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,0),3)

        _, jpeg = cv2.imencode('.jpg', img)
        return jpeg.tobytes()
        
