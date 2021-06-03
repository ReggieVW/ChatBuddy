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


# Server Python script:
To run the server
 <code>
 python server.py
 </code>
 </p>

 
 # Dataset Face Sentiment:
 
For emotion detection the Kaggle dataset is used. This dataset can be used to detect 5 facial emotions as listed below:
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
 ![image](https://user-images.githubusercontent.com/35894891/120638574-9596c780-c470-11eb-8e76-5f190bd3d792.png)

