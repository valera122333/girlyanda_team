import os
import cv2
from PIL import Image
import numpy as np


current_dir = os.getcwd()


category_mapping = {
    "CK20.01.01.01.406": 0,
    "CK20.01.01.02.402": 1,
    "CK30.01.01.02.402": 2,
    "CK30.01.01.03.403": 3,
    "CK50.01.01.404": 4,
    "CK50.02.01.411": 5,
    "CS120.01.413": 6,
    "CS120.07.442": 7,
    "CS150.01.427-01": 8,
    "CVM.37.060": 9,
    "CVM.37.060A": 10,
    "CVP-120.00.060": 11,
    "CVP120.42.020": 12,
    "CVP120.42.030": 13,
    "SPO250.14.190": 14,
    "SU80.01.426": 15,
    "SU80.10.409A": 16,
    "SU160.00.404": 17,
    "ZVT86.103K-02": 18,
}


data = []
labels = []


for category, label in category_mapping.items():
    category_dir = os.path.join(current_dir, "CNN/data", category)
    
    
    if not os.path.exists(category_dir):
        print(f"Directory {category_dir} does not exist.")
        continue

   
    for filename in os.listdir(category_dir):
        try:
            image_path = os.path.join(category_dir, filename)
            imag = cv2.imread(image_path)

           
            if imag is None:
                print(f"Failed to load image: {image_path}")
                continue

            img_from_ar = Image.fromarray(imag, 'RGB')
            resized_image = img_from_ar.resize((50, 50))
            data.append(np.array(resized_image))
            labels.append(label)
        except Exception as e:
            print(f"Error processing {image_path}: {e}")


details = np.array(data)
labels = np.array(labels)

 
np.save("details", details)
np.save("labels", labels)