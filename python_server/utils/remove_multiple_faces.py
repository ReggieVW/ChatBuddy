import cv2
import numpy as np
import shutil
import os
import unidecode

for subdir, dirs, files in os.walk("\\images\\"):
    for file in files:
        filepath = subdir + os.sep + file

        if filepath.endswith(".jpg"):
            print (filepath)
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
            try:
                img = cv2.imread(filepath)
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                count_faces=str(len(faces))
                print("number of face(s)= " + count_faces)
                if(1 != len(faces)):
                    print("file removed " + filepath)
                    os.remove(filepath)
            except:
                print("error" +filepath)

