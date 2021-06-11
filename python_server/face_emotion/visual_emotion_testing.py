from keras.models import load_model
from time import sleep
from keras.preprocessing.image import img_to_array
from keras.preprocessing import image
import cv2
import numpy as np

# initialize the Haar Cascade face detection model
face_haar_cascade = cv2.CascadeClassifier(cv2.samples.findFile(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'))

model =load_model(r'Emotion_face.h5')
video_capture = cv2.VideoCapture(0)

class_labels = ['Angry','Happy','Neutral','Sad','Surprise']
loop_break = True

while loop_break:
    ret,img=video_capture.read()# captures frame and returns boolean value and captured image
    if not ret or img is None:
        continue
    if cv2.waitKey(10) == ord('q'):#wait until 'q' key is pressed
        print("pressed 'q'")
        loop_break = False
        # When everything is done, release the capture
        break
    gray= cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces_detected = face_haar_cascade.detectMultiScale(gray, 1.32, 5)

        
    if len(faces_detected) != 0:
        
        for (x,y,w,h) in faces_detected:
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
            else:
                cv2.putText(img,'No Face Found',(20,60),cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,0),3)

    resized_img = cv2.resize(img, (1000, 700))
    cv2.imshow('Facial emotion analysis ',resized_img)


# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()


























