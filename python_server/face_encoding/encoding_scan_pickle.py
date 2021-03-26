import re
from imutils import paths
from face_encoding.encoding_scan import FaceEncoding
import face_recognition
import uuid
import pickle
import cv2
import os

class FaceEncodingPickle(FaceEncoding):
    
    def __init__(self, known_people_folder):
        self.known_people_folder = known_people_folder
    
    def load_encodings(self):
        if not os.path.isfile('face_enc'):
            return [],[]
        # load the known faces and embeddings saved in last file
        data = pickle.loads(open('face_enc', "rb").read())
        return data["encodings"], data["names"]
    
    def add_images(self, images, name):
        for image in images:
            self.add_image(image, name)          

    def add_image(self, image, name):
        # Saving the image
        super().add_image(image, name)
        # Saving the encodings
        knownEncodings, knownNames = self.load_encodings()
        try:
            img_enc = face_recognition.face_encodings(image)[0]##Encodings
        except IndexError as e:
            return
        knownEncodings.append(img_enc)
        knownNames.append(name)
        data = {"encodings": knownEncodings, "names": knownNames}
        #use pickle to save data into a file for later use
        f = open("face_enc", "wb")
        f.write(pickle.dumps(data))
        f.close()

    def dump_full_encodings(self):
        known_names, known_face_encodings = super().load_encodings()
        #save emcodings along with their names in dictionary data
        data = {"encodings": known_face_encodings, "names": known_names}
        #use pickle to save data into a file for later use
        f = open("face_enc", "wb")
        f.write(pickle.dumps(data))
        f.close()
        
    def scan_images(self, images_to_check):
        for image in images_to_check:
            name = self.scan_image(image)
            if name != "unknown":
                break
        return name

    def scan_image(self, image_to_check):
        knownEncodings = []
        knownNames = []
        try:
            img_enc = face_recognition.face_encodings(image_to_check)[0]##Encodings
        except IndexError as e:
            return "unknown"
        knownEncodings, knownNames = self.load_encodings()
        results = face_recognition.compare_faces(knownEncodings,img_enc)
        name = "unknown"
        for i in range(len(results)):
            if results[i]:
                name = knownNames[i]
        return name


#path = os.getcwd()
#print(path)
#faceRecog = FaceEncodingPickle("../known_faces")
#faceRecog.dump_full_encodings()
#image = cv2.imread("00050.jpg")
#print(faceRecog.scan_image(image))