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


def train(train_dir, model_save_path):
    X = []
    y = []
    # Loop through each person in the training set
    for class_dir in os.listdir(train_dir):
        if not os.path.isdir(os.path.join(train_dir, class_dir)):
            continue
        # Loop through each training image for the current person
        for img_path in image_files_in_folder(os.path.join(train_dir, class_dir)):
            image = face_recognition.load_image_file(img_path)
            face_bounding_boxes = face_recognition.face_locations(image)
            if len(face_bounding_boxes) != 1:
                # If there are no people (or too many people) in a training image, skip the image.
                if verbose:
                    print("Image {} not suitable for training: {}".format(img_path, "Didn't find a face" if len(face_bounding_boxes) < 1 else "Found more than one face"))
            else:
                # Add face encoding for current image to the training set
                X.append(face_recognition.face_encodings(image, known_face_locations=face_bounding_boxes)[0])
                y.append(class_dir)
                
    # Create and train the KNN classifier
    knn_clf = neighbors.KNeighborsClassifier(n_neighbors=1, algorithm='ball_tree', weights='distance')
    knn_clf.fit(X, y)

    # Save the trained KNN classifier
    with open(model_save_path, 'wb') as f:
        pickle.dump(knn_clf, f)

    return knn_clf


def predict(X_img_path, model_path, distance_threshold=0.6):

    with open(model_path, 'rb') as f:
        knn_clf = pickle.load(f)

    # Load image file and find face locations
    X_img = face_recognition.load_image_file(X_img_path)
    X_face_locations = face_recognition.face_locations(X_img)


    # If no faces are found in the image, return the predicted face location 
    if len(X_face_locations) == 0:
        return []

    # Find encodings for faces in the test iamge
    faces_encodings = face_recognition.face_encodings(X_img, known_face_locations=X_face_locations)

    # Use the KNN model to find the best matches for the test face
    closest_distances = knn_clf.kneighbors(faces_encodings, n_neighbors=1)
    are_matches = [closest_distances[0][i][0] <= distance_threshold for i in range(len(X_face_locations))]

    # Predict classes and remove classifications that aren't within the threshold
    return [(pred, loc) if rec else ("unknown", loc) for pred, loc, rec in zip(knn_clf.predict(faces_encodings), X_face_locations, are_matches)]


if __name__ == "__main__":
    # STEP 1: Train the KNN classifier and save it to disk
    # Once the model is trained and saved, you can skip this step next time.
    print("KNN Classifier is being trained")
    classifier = train("images-train", model_save_path="trained_knn_model.clf")
    print("Traing is done. You can use the trained model to predict ur test data now. ")

    result = [['image_label', 'name']]
    count = 0
    # STEP 2: Using the trained classifier, make predictions for unknown images
    for image_file in os.listdir("images-val-pub"):
        print(image_file)
        count +=1
        if count % 100 == 0: print ("Processed {} images".format(count))
        full_file_path = os.path.join("images-val-pub", image_file)
        predictions = predict(full_file_path, "trained_knn_model.clf")
        append_helper = [str(image_file), predictions[0][0]]
        result.append(append_helper)
print(result)
