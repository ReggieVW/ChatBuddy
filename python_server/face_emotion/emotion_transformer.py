import cv2
import numpy as np
from keras.models import model_from_json
from keras.preprocessing import image
from keras.models import load_model
from keras.preprocessing.image import img_to_array  
from datetime import datetime   
import pathlib	
import os

# initialize the Haar Cascade face detection model
face_haar_cascade = cv2.CascadeClassifier(cv2.samples.findFile(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'))
#load weights
filepath = pathlib.Path(__file__).resolve().parent 
model =load_model(os.path.join(filepath, 'Emotion_face.h5'))

class_labels = ['Angry', 'Happy', 'Neutral', 'Sad', 'Surprise']

class EmotionImage:
    def transform(img):
        label = "unknown"
        gray= cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces_detected = face_haar_cascade.detectMultiScale(gray, 1.32, 5)
        print("face detected= "+ str(faces_detected))
        if len(faces_detected) == 0:
            cv2.putText(img,"No face detected",(50,50),cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,0),3)
        if len(faces_detected) != 0:
            for (x, y, w, h) in faces_detected:
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),thickness=1)
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
                    now = datetime.now()
                    current_time = now.strftime("%H:%M:%S")
                    cv2.putText(img,"Angry : " + "{0:.0%}".format(preds[0]),(x-200,y+50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),3)
                    cv2.putText(img,"Happy : " + "{0:.0%}".format(preds[1]),(x-200, y+80),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),3)
                    cv2.putText(img,"Neutral : " + "{0:.0%}".format(preds[2]),(x-200,y+110),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),3)
                    cv2.putText(img,"Sad : " + "{0:.0%}".format(preds[3]),(x-200,y+140),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),3)
                    cv2.putText(img,"Surprise : " + "{0:.0%}".format(preds[4]),(x-200,y+170),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),3)
        return img, label

#img = cv2.imread("1622296082_pred.jpg")
#transformed_img = SentimentImage.transform(img)
# Filename
#filename = 'savedImage.jpg'
#Using cv2.imwrite() method
# Saving the image
#cv2.imwrite(filename, transformed_img)
