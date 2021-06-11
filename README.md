# ChatBuddy
ChatBuddy uses artificial intelligence to contribute to the well-being of the elderly persons. 

# System Overview
![system_overview_5](https://user-images.githubusercontent.com/35894891/121050643-09123f00-c7b9-11eb-9572-bc1e9216168c.png)


# Frontend React
<p>
 <code>
 npm install
 </code>
  Install the dependencies in the node_modules folder.
 </p>
 <p>
  <code>
 npm start
 </code>
 Runs the web app on http://localhost:3000/
 </p>
 
 Tested with Chrome, Edge and Firefox

# Server Python 
To run the server on http://localhost:5000/ </br>
 <code>
 python server.py
 </code>
 </p>
 
 ## Dependencies Python
 Supported for Python 3.8 </br>
  <code>
 cd python_server    
   </code>
   (cmd)
   </br>
 <code>
  pip install -r requirements.txt 
  </code>
  
  dependencies:
  
  - numpy </br>
  - opencv-python</br>
  - dlib  (Install Visual Studio with C++ compiler)</br>
  - keras</br>
  - pandas</br>
  - tensorflow (TensorFlow 2.x is on 4/21 supported on the following 64-bit systems: Python 3.5–3.8)</br>
  - Pillow</br>
  - flask</br>
  - flask_cors</br>
  - cMake (Install Visual Studio with C++ compiler)</br>
  - face_recognition</br>
  - imutils</br>
  - mediapipe</br>
  - sklearn</br>
  - nltk</br>
  - emoji</br>

Tested with Python 3.8.8, 3.8.10 Make sure to install the C++ compiler!</br>
For Python 3.8 on Windows 10 | Cmake | Dlib =>
https://www.youtube.com/watch?v=xaDJ5xnc8dc  
 
 ## Dataset Face Emotion Detection
 
For emotion detection the Kaggle dataset is used. This dataset we use to detect 5 facial emotions as listed below:
'angry': 0, 'happy': 1, 'neutral': 2, 'sad': 3, 'surprise': 4
 https://www.kaggle.com/jonathanoheix/face-expression-recognition-dataset
![image](https://user-images.githubusercontent.com/35894891/120637921-c4f90480-c46f-11eb-849f-fdec1e220af9.png)
</br>
![image](https://user-images.githubusercontent.com/35894891/120635837-308da280-c46d-11eb-9725-ecef418a7513.png)
</br>
 Web scraping is used for more specific images using Selenium.

1) Launch chrome browser:
2) Enter specific term in google image search box
3) Find (scroll to) the image and click
4) Extract the link from the image popup
5) Save image to destination
6) Exclude: count faces != 1
7) Convert to grayscale and use same dimensions as Kaggle dataset
 <code>
 cd python_server/utils
 </code>
 (cmd) 
 </br>

  <code>
python scrapper_main.py
 </code>
 (step 1, 2, 3, 4, 5)
 </br>
  <code>
python remove_multiple_faces.py
 </code>
 (step 6)
 </br>
  <code>
python resize_images.py
 </code>
 (step 7)
 </br>
 
## Face Emotion Detection – Training (CNN)
 
![image](https://user-images.githubusercontent.com/35894891/120776271-5629b300-c524-11eb-80c0-7869df8434d3.png)
 
Evaluation accuracy and training loss:
The validation accuracy starts to stabilize at the end of the 23 epochs between 60% and 70% accuracy.

 <code>
 cd python_server/face_emotion
  </code>
(cmd) 
   </br>
   <code>
python visual_emotion_training.py
 </code>

## Face Emotion Detection – Webcam

The implementation of our model on a webcam:
1) Take each frame of the video image by image (using OpenCV).
2) Apply a grayscale filter to reduce inputs.
3) Reduce pixel density to the same as the trained set.
4) Detect the face (using haarcascade_frontalface_default.xml).
5) Use model to predict the emotion of the input (Keras/TensorFlow).
 <code>
 cd python_server/face_emotion
   </code>
(cmd) 
   </br>
   <code>
python visual_emotion_testing.py
 </code>
 </br>
 
## Face Recognition

Face recognition process:
1) Capture a face (using Haar feature based cascade classifiers XML)
2) Create own (small) dataset with faces
3) Quantify the image dataset
4) Store encodings
5) Compare encodings with new face
6) Use KNN to make the final face classification
 </br>
 
 ![Afbeelding1](https://user-images.githubusercontent.com/35894891/120645316-929fd500-c478-11eb-8ca0-c6cac8bdf251.jpg)

 </br>
 <code>
 cd python_server/face_encoding
   </code>
(cmd) 
   </br>
  </br>
     <code>
python face_recognition_knn_training.py
 </code>
 </br>
   <code>
python face_recognition_testing.py
 </code>
 </br>

## Eliza Chatbot

a) 1964 at MIT Artificial Intelligence Laboratory by Joseph Weizenbaum.

b) A therapist chatbot.

c) Uses a "pattern matching" and substitution methodology.

d) Claims passing the Turing Test in the 60's.

 <code>
 cd python_server/eliza
  </code>
(cmd) 
   </br>
   <code>
python eliza.py
 </code>




