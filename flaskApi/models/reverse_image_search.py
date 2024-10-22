import pickle
import tensorflow as tf
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

# Global variables to load only once
model = None
feature_list = None
filenames = None
neighbors = None

# Function to initialize model and data
def initialize_model_and_data():
    global model, feature_list, filenames, neighbors
    # Load the pickle files only once
    feature_list = np.array(pickle.load(open('models/embeddings.pkl', 'rb')))
    filenames = pickle.load(open('models/filenames.pkl', 'rb'))

    # Load the model once
    base_model = ResNet50(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    base_model.trainable = False
    model = tf.keras.Sequential([
        base_model,
        GlobalMaxPooling2D()
    ])
    
    # Initialize NearestNeighbors only once
    neighbors = NearestNeighbors(n_neighbors=2, algorithm='brute', metric='euclidean')
    neighbors.fit(feature_list)

# Call this function once when the app starts
initialize_model_and_data()

def get_image_recommendation(image_url):
    # Model and pickled data are already initialized
    response = requests.get(image_url)
    img = image.load_img(BytesIO(response.content), target_size=(224, 224))
    img_array = image.img_to_array(img)
    expanded_img_array = np.expand_dims(img_array, axis=0)
    preprocessed_img = preprocess_input(expanded_img_array)
    
    # Predict the image embedding using the preloaded model
    result = model.predict(preprocessed_img).flatten()
    normalized_result = result / norm(result)
    
    # Find the nearest neighbors
    distances, indices = neighbors.kneighbors([normalized_result])

    # Retrieve the recommended image file name
    for file in indices[0][1:2]:
        temp_img = cv2.imread(filenames[file])
        file_name = filenames[file]
        numeric_part = file_name.split('/')[-1].split('.')[0]
        print(numeric_part)
    return numeric_part