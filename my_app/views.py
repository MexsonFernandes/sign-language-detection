from django.shortcuts import render,redirect
from binascii import a2b_base64
from io import BytesIO
from PIL import Image
import cv2
import numpy as np
import keras
from keras_applications import vgg16
from keras.models import load_model
from keras import applications
from keras import backend as K
import numpy as np
from keras.models import Model
from keras.layers import Dropout, Flatten, Dense
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt


def openCamera(request):
    return render(request, 'camera.html')

import tensorflow as tf
graph = tf.get_default_graph()
label = ''

#Defining labels 
def get_label(argument):
    labels = {0:'Angry', 1:'A', 2:'Add', 3:'Afraid', 4:'B' , 5:'Bent', 6:'Between', 7:'Blind', 8:'Bottle', 9:'Bowl', 10:'Brain', 
        11:'Bud', 12:'C', 13:'Chest', 14:'Claw', 15:'Cough', 16:'Cow', 17:'D', 18:'Devil', 19:'Doctor', 20:'East', 21:'Eight', 
        22:'Elbow', 23:'Evening', 24:'Eye', 25:'F', 26:'Faith', 27:'Fat', 28:'Feel', 29:'Fever', 30:'Few', 31:'Fist', 32:'Five', 
        33:'Food', 34:'Four', 35:'G', 36:'Good', 37:'Gun', 38:'Hair', 39:'Hand', 40:'Head', 41:'Hear', 42:'I', 43:'Jain', 44:'K', 
        45:'King', 46:'L', 47:'Leprosy', 48:'Love', 49:'M', 50:'Me', 51:'N', 52:'Nine', 53:'Nose', 54:'Nurse', 55:'O', 56:'Oath', 57:'One', 58:'Open', 59:'Owl', 60:'P', 61:'Police', 62:'Pray', 63:'Promise', 64:'q', 65:'R', 66:'S', 67:'Seven', 68:'Shirt', 69:'Shoulder', 70:'Sick', 71:'Six', 72:'Skin', 73:'Sleep', 74:'Soldier', 75:'Stand', 76:'Strong', 77:'Sunday', 78:'T', 79:'Telephone', 80:'Ten', 81:'Thorn', 82:'Thumbs_up', 83:'Trouble', 84:'Two', 85:'U', 86:'W', 87:'Water', 88:'Wedding', 89:'West', 90:'White', 91:'Word', 92:'X', 93:'You', 94:'Z' }
    return(labels.get(argument, "Invalid emotion"))


@csrf_exempt
def detect(request):
    #Using another pre-trained model because of it's better accuracy
    img_width, img_height = 150, 150 # Resolution of inputs
    
    # Load INCEPTIONV3
    model=applications.InceptionV3(weights=None, include_top=False, 
                                   input_shape=(img_width, img_height, 3))
    # Freeze first 15 layers
    for layer in model.layers[:45]:
        layer.trainable = False
    for layer in model.layers[45:]:
       layer.trainable = True
        
    # Attach additional layers
    x = model.output
    x = Flatten()(x)
    x = Dense(1024, activation="relu")(x)
    x = Dropout(0.5)(x)
    x = Dense(1024, activation="relu")(x)
    x = Dropout(0.5)(x)
    predictions = Dense(100, activation="softmax")(x) # 4-way softmax classifier at the end
    
    my_model = Model(inputs=model.input, outputs=predictions)
    my_model.load_weights(settings.MEDIA_ROOT + "/model.h5")
        
    data = ''
    res_type = request.POST.get('res', '')

    #Getting image
    try:
        data = request.POST['image_data']
    except:
        K.clear_session()
        #No data, redirect to openCamera
        return redirect(openCamera)

    #Decoding image URI
    binary_data = a2b_base64(data)
    image_data = BytesIO(binary_data)

    img = np.array(Image.open(image_data))

    #Resizing image to required size and processing
    width = 150
    height = 150
    img_stack_sm = np.zeros((3, width, height))
    
    for idx in range(3):
        img_t = img[idx, :, :]
        img_sm = cv2.resize(img_t, (width, height), interpolation=cv2.INTER_CUBIC)
        img_stack_sm[idx, :, :] = img_sm

    #test_image = cv2.resize(img, (150,150,3))
    test_image = np.array(img_stack_sm)
    
    #scale pixels values to lie between 0 and 1 because we did same to our train and test set
    

    #reshaping image (-1 is used to automatically fit an integer at it's place to match dimension of original image)
    gray = test_image.reshape(-1, 150, 150, 3)

    res = my_model.predict(gray)

    #argmax returns index of max value
    result_num = np.argmax(res)

    label = get_label(result_num)
    print(label)
    if res_type == 'json':
        print('json')
        return JsonResponse({"result": True, "label": label})
    return render(request, 'main2.html' , {'label': label} )
    