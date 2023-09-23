import os
import cv2
from PIL import Image
import numpy as np
import tensorflow as tf

imag=cv2.imread(os.getcwd() +'/CNN/testpapka/IMG_20230919_141913.jpg')
img_from_ar = Image.fromarray(imag, 'RGB')
resized_image = img_from_ar.resize((50, 50))
test_image =np.expand_dims(resized_image, axis=0)  
model = tf.keras.models.load_model(os.getcwd() + '/model.h5')
result = model.predict(test_image) 
print(result) 
print("Result is: ", (result[0][np.argmax(result)])/100,'%')
print("Prediction: " + str(np.argmax(result)))

for i in result.flat:
   print(i)

 
