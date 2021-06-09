"""
@Author Adam Geitgey
with some updates by Reginald Van Woensel
"""
import numpy as np
import cv2
import face_recognition
import pickle

def predict(frame, knn_clf=None, model_path=None, distance_threshold=0.6):

    if knn_clf is None and model_path is None:
        raise Exception("Must supply knn classifier either thourgh knn_clf or model_path")

    # Load a trained KNN model (if one was passed in)
    if knn_clf is None:
        with open(model_path, 'rb') as f:
            knn_clf = pickle.load(f)

    # find face locations from frame
    X_face_locations = face_recognition.face_locations(frame)

    # If no faces are found in the image, return an empty result.
    if len(X_face_locations) == 0:
        return []

    # Find encodings for faces in the frame
    faces_encodings = face_recognition.face_encodings(frame, known_face_locations=X_face_locations)

    # Use the KNN model to find the best matches for the test face
    closest_distances = knn_clf.kneighbors(faces_encodings, n_neighbors=1)
    are_matches = [closest_distances[0][i][0] <= distance_threshold for i in range(len(X_face_locations))]

    # Predict classes and remove classifications that aren't within the threshold
    return [(pred, loc) if rec else ("unknown", loc) for pred, loc, rec in zip(knn_clf.predict(faces_encodings), X_face_locations, are_matches)]


def show_labels_on_webcam(RGBFrame, predictions):

    frame = RGBFrame

    for name, (top, right, bottom, left) in predictions:
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        print (frame.shape)
        print (frame.dtype)
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)


    # Display the resulting image
    cv2.imshow('Video', frame)

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()
    if cv2.waitKey(10) == ord('q'):#wait until 'q' key is pressed
        print("pressed 'q'")
        loop_break = False
        # When everything is done, release the capture
        break

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    predictions = predict(rgb_small_frame, model_path="trained_knn_model.clf")

    # Display results overlaid on webcam video
    print (rgb_small_frame.shape)
    print (rgb_small_frame.dtype)
    show_labels_on_webcam(frame, predictions)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()