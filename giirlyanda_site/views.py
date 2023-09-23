import os
import cv2
from PIL import Image
import numpy as np
import tensorflow as tf
from django.conf import settings
from django.template.response import TemplateResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.core.files.storage import FileSystemStorage

class CustomFileSystemStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        self.delete(name)
        return name

def index(request):
    message = ""
    fss = CustomFileSystemStorage()
    try:
        image = request.FILES["image"]
        print("Name", image.file)
        _image = fss.save(image.name, image)
        path = str(settings.MEDIA_ROOT) + "/" + image.name
        # image details
        image_url = fss.url(_image)
        # Read the image
        imag=cv2.imread(path)
        img_from_ar = Image.fromarray(imag, 'RGB')
        resized_image = img_from_ar.resize((50, 50))
        test_image =np.expand_dims(resized_image, axis=0) 
        model = tf.keras.models.load_model(os.getcwd() + '/model.h5')
        result = model.predict(test_image) 

        values = result[0]
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

        valu = []
        for i in result.flat:
            valu.append(i)

        detail_percentages = []
        for category, index in category_mapping.items():
            percentage = 0
            if valu[index] <= -1000 and valu[index] >= -10000:
                percentage = (valu[index]+10000)/2000
                detail_percentages.append({"name": category, "percentage": percentage})
            elif valu[index] <= -100 and valu[index] >= -999:
                percentage = (valu[index]+1000)/200
                detail_percentages.append({"name": category, "percentage": percentage})
            elif valu[index] <= -10 and valu[index] >= -99:
                percentage = (valu[index]+100)/10
                detail_percentages.append({"name": category, "percentage": percentage})
            elif valu[index] <= 0 and valu[index] >= -9:
                percentage = (valu[index]+100)/10
                detail_percentages.append({"name": category, "percentage": percentage})
            elif valu[index] >= 0 and valu[index] <= 9:
                percentage = (valu[index]+100)/10
                detail_percentages.append({"name": category, "percentage": percentage})
            elif valu[index] >= 10 and valu[index] <= 99:
                percentage = (valu[index]+100)/10
                detail_percentages.append({"name": category, "percentage": percentage})
            elif valu[index] >= 100 and valu[index] <= 999:
                percentage = (valu[index]+10000)/200
                detail_percentages.append({"name": category, "percentage": percentage})
            elif valu[index] >= 1000 and valu[index] <= 10000:
                percentage = (valu[index]+10000)/200
                detail_percentages.append({"name": category, "percentage": percentage})
                
        detail_percentages.sort(key=lambda x: x["percentage"], reverse=True)

        max_percentage = 0
        max_category = None
    
        for item in detail_percentages:
            percentage = item["percentage"]
            if percentage > max_percentage:
                max_percentage = percentage
                max_category = item["name"]
                
            print("" + max_category)

        return TemplateResponse(
            request,
            "index.html",
            {
                "message": message,
                "image": image,
                "image_url": image_url,
                
                "values": values,
                "category_mapping": category_mapping,
                "detail_percentages": detail_percentages,
                "max_category":max_category,   
            },
        )
    except MultiValueDictKeyError:
        return TemplateResponse(
            request,
            "index.html",
            {"message": "Загрузите изображение"},
        )
