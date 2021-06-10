"""
@Author Adam Geitgey
with some updates by Reginald Van Woensel
"""


import math
from sklearn import neighbors
import os
import os.path
import pickle
import face_recognition
from face_recognition.face_recognition_cli import image_files_in_folder
import csv
import cv2
import uuid


def train(train_dir, trained_model):
    print('training')
    X_train = []
    y_label = []
    # Loop through each person
    for label_dir in os.listdir(train_dir):
        print('Loop through each person: '+label_dir)
        if not os.path.isdir(os.path.join(train_dir, label_dir)):
            continue
        # Loop through each image 
        for img_path in image_files_in_folder(os.path.join(train_dir, label_dir)):
            image = face_recognition.load_image_file(img_path)
            face_boxes = face_recognition.face_locations(image)
            if len(face_boxes) != 1:
                # If there are no people (or too many people) in the image
                print("Image {} not suitable for training: {}".format(img_path, "Didn't find a face" if len(face_bounding_boxes) < 1 else "Found more than one face"))
            else:
                # Add face encoding 
                X_train.append(face_recognition.face_encodings(image, known_face_locations=face_boxes)[0])
                y_label.append(label_dir)
                
    # Create and train the KNN classifier
    # The Ball Tree Algorithm can be contemplated as a metric tree.
    knn_clf = neighbors.KNeighborsClassifier(n_neighbors=1, algorithm='ball_tree', weights='distance')
    knn_clf.fit(X_train, y_label)

    # Save the trained KNN classifier
    with open(trained_model, 'wb') as f:
        pickle.dump(knn_clf, f)
        print("dump file "+trained_model)

    return knn_clf
    
    
def add_image(train_dir, image, name):
    # Saving the image
    directory = train_dir + "/" + name
    filename = str(uuid.uuid4()) + '.jpg'
    try:
        if not os.path.exists(directory):
            os.mkdir(directory)
    except OSError:
        print ("Creation of the directory %s failed" % directory)
    else:
        print ("Successfully created the directory %s " % directory)
    cv2.imwrite(os.path.join(directory, filename), image) 


def predict_face(img_path, trained_model, distance_threshold=0.6):

    if not os.path.exists(trained_model):
        return []

    with open(trained_model, 'rb') as f:
        knn_clf = pickle.load(f)

    # Load image file and detect face
    image = face_recognition.load_image_file(img_path)
    face_detected = face_recognition.face_locations(image)

    # If no faces are found  
    if len(face_detected) == 0:
        return []

    # Find encodings for faces 
    faces_encodings = face_recognition.face_encodings(image, known_face_locations=face_detected)

    # Use the KNN model to find the best matches
    closest_distances = knn_clf.kneighbors(faces_encodings, n_neighbors=1)
    matches = [closest_distances[0][i][0] <= distance_threshold for i in range(len(face_detected))]

    # Predict labels and remove labels that aren't within the threshold
    return [(pred, loc) if rec else ("unknown", loc) for pred, loc, rec in zip(knn_clf.predict(faces_encodings), face_detected, matches)]


if __name__ == "__main__":
    # STEP 1: Train the KNN classifier and save it to disk
    # Once the model is trained and saved, you can skip this step next time.
    print("KNN Classifier is being trained")
    classifier = train("images-train", "trained_knn_model.clf")
    print("Traing is done. You can use the trained model to predict")

    result = [['image_label', 'name']]
    count = 0
    # STEP 2: Using the trained classifier, make predictions for unknown images
    for image_file in os.listdir("images-val-pub"):
        print(image_file)
        count +=1
        if count % 100 == 0: print ("Processed {} images".format(count))
        full_file_path = os.path.join("images-val-pub", image_file)
        predictions = predict_face(full_file_path, "trained_knn_model.clf")
        append_helper = [str(image_file), predictions[0][0]]
        result.append(append_helper)
    print(result)
