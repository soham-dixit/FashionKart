import pickle
import tensorflow
import numpy as np
from numpy.linalg import norm
from tensorflow.keras.preprocessing import image
from tensorflow.keras.layers import GlobalMaxPooling2D
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from sklearn.neighbors import NearestNeighbors
import cv2
import os
import requests
from io import BytesIO

def get_image_recommendation(image_url):
    feature_list = np.array(pickle.load(open('models/embeddings.pkl','rb')))
    filenames = pickle.load(open('models/filenames.pkl','rb'))

    model = ResNet50(weights='imagenet',include_top=False,input_shape=(224,224,3))
    model.trainable = False

    model = tensorflow.keras.Sequential([
        model,
        GlobalMaxPooling2D()
    ])
    
    response = requests.get(image_url)
    img = image.load_img(BytesIO(response.content), target_size=(224, 224))
    img_array = image.img_to_array(img)
    expanded_img_array = np.expand_dims(img_array, axis=0)
    preprocessed_img = preprocess_input(expanded_img_array)
    result = model.predict(preprocessed_img).flatten()
    normalized_result = result / norm(result)

    neighbors = NearestNeighbors(n_neighbors=2,algorithm='brute',metric='euclidean')
    neighbors.fit(feature_list)

    distances,indices = neighbors.kneighbors([normalized_result])

    for file in indices[0][1:2]:
        temp_img = cv2.imread(filenames[file])
        file_name = filenames[file]
        numeric_part = file_name.split('/')[-1].split('.')[0]
        print(numeric_part)
    return numeric_part
