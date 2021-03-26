import re
from imutils import paths
import face_recognition
import uuid
import pickle
import cv2
import os

class FaceEncoding:

    def __init__(self, known_people_folder):
        self.known_people_folder = known_people_folder

    def load_encodings(self):
        known_people_folder = self.known_people_folder
        imagePaths = list(paths.list_images(known_people_folder))
        known_face_encodings = []
        known_names = []
        # loop over the image paths
        for (i, imagePath) in enumerate(imagePaths):
            # extract the person name from the image path
            basename = imagePath.split(os.path.sep)[-2]
            img = face_recognition.load_image_file(imagePath)
            encodings = face_recognition.face_encodings(img)
            if len(encodings) > 1:
                click.echo("WARNING: More than one face found in {}. Only considering the first face.".format(file))
            if len(encodings) == 0:
                click.echo("WARNING: No faces found in {}. Ignoring file.".format(file))
            else:
                known_names.append(basename)
                known_face_encodings.append(encodings[0])
        return known_names, known_face_encodings

    def add_image(self, image, name):
        known_people_folder = self.known_people_folder
        # Saving the image
        directory = known_people_folder + "/" + name
        filename = str(uuid.uuid4()) + '.jpg'
        try:
            if not os.path.exists(directory):
                os.mkdir(directory)
        except OSError:
            print ("Creation of the directory %s failed" % directory)
        else:
            print ("Successfully created the directory %s " % directory)
        cv2.imwrite(os.path.join(directory, filename), image) 

    def scan_image(self, images_to_check):
        known_people_folder = self.known_people_folder
        if not os.path.exists(known_people_folder):
            print("created directory: " + known_people_folder)
            os.makedirs(known_people_folder)
        try:
            img_enc = face_recognition.face_encodings(images_to_check)[0]##Encodings
            known_names, known_face_encodings = self.load_encodings()
            results = face_recognition.compare_faces(known_face_encodings,img_enc)
        except IndexError as e:
             print('no face detected')
        name = "unknown"
        for i in range(len(results)):
            if results[i]:
                name = known_names[i]
        return name

#faceRecog = FaceEncoding("known_faces")
#image = cv2.imread("00050.jpg")
#print(faceRecog.scan_image(image))
