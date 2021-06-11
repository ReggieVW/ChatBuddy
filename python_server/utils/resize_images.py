import cv2
from PIL import Image 
import PIL
import os
 
for subdir, dirs, files in os.walk(r'\\images\\'):
    for filename in files:
        filepath = subdir + os.sep + filename

        if filepath.endswith(".jpg") or filepath.endswith(".png"):
            print (filepath) 
            img = cv2.imread(filepath, cv2.IMREAD_UNCHANGED)
            print('Original Dimensions : ',img.shape)
            width = 48
            height = 48
            dim = (width, height)
            # resize image
            gray= cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            resized = cv2.resize(gray, dim, interpolation = cv2.INTER_AREA)
            print('Resized Dimensions : ',resized.shape)
            # save image 
            result=cv2.imwrite(filepath, resized)
 