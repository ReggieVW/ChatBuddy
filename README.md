# ChatBuddy
ChatBuddy uses artificial intelligence to contribute to the well-being of the elderly persons. 
It integrates video processing, sound processing & chat to interact with the user. 

# Dependencies Python
<code>
pip install numpy
</code>
</p>
<code>
pip install opencv-python
</code>
</p>
<code>
pip install keras
</code>
</p>
<code>
pip install pandas
</code>
<code>
</p>
pip install tensorflow
</code>
TensorFlow is now (3/21) supported on the following 64-bit systems: Python 3.5–3.8.
</p>
<p>
<code>
pip install Pillow
 </code>
</p>
<p>
<code>
pip install flask
 </code>
</p>
<p>
<code>
pip install flask_cors
 </code>
</p>
<p>
<code>
pip install cMake
 </code>
  Install Visual Studio with C++ compiler.
</p>
<p>
<code>
pip install face_recognition
 </code>
</p>
<p>
<code>
pip install imutils
 </code>
 </p>
<p>
 <code>
pip install mediapipe
</code>
</p>

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


# Server Python 
To run the server
 <code>
 python server.py
 </code>
 </p>

 
 ## Dataset Face Sentiment
 
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
 cd utils
 </code>
 </br>
  <code>
python scrapper_main.py
 </code>
 </br>
  <code>
python remove_multiple_faces.py
 </code>
 </br>
  <code>
python resize_images.py
 </code>
 </br>
 
## Face Sentiment Analysis – Training (CNN)
 
![image](https://user-images.githubusercontent.com/35894891/120639691-ec50d100-c471-11eb-947e-7a29bdee2ee5.png)
 
Evaluation accuracy and training loss:
The validation accuracy starts to stabilize at the end of the 23 epochs between 50% and 60% accuracy.

 <code>
 cd python_server/face_sentiment
  </code>
   </br>
   <code>
python visual_emotion_training.py
 </code>

## Face Sentiment Analysis – Webcam

The implementation of our model on a webcam:
1) Take each frame of the video image by image (using OpenCV).
2) Apply a grayscale filter to reduce inputs.
3) Reduce pixel density to the same as the trained set.
4) Detect the face (using haarcascade_frontalface_default.xml).
5) Use model to predict the emotion of the input (Keras/TensorFlow).
 <code>
 cd python_server/face_sentiment
   </code>
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
   </br>
   <code>
python face_recognition_knn_training.py
 </code>
  </br>
   <code>
python face_recognition_testing.py
 </code>
 </br>

## Eliza 

a) 1964 at MIT Artificial Intelligence Laboratory by Joseph Weizenbaum.

b) Is a therapist chatbot.

c) Using a "pattern matching" and substitution methodology.

d) Claims passing the Turing Test in the 60's.

 <code>
 cd python_server/eliza
  </code>
   </br>
   <code>
python eliza.py
 </code>




